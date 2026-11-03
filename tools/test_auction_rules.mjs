// Firestore rules tests for the Code Auction (and a check that the per-user docs stay locked).
// Run from an empty folder with firebase-tools, @firebase/rules-unit-testing and firebase installed, and firestore.rules copied in:
//   npx firebase emulators:exec --only firestore --project demo-codebay "node test_auction_rules.mjs"
// with firebase.json = {"firestore":{"rules":"firestore.rules"},"emulators":{"firestore":{"port":8085}}}. Needs Java.
import { initializeTestEnvironment, assertSucceeds, assertFails } from "@firebase/rules-unit-testing";
import { doc, getDoc, setDoc, updateDoc, writeBatch, Timestamp, serverTimestamp, addDoc, collection, getDocs, deleteDoc } from "firebase/firestore";
import { readFileSync } from "fs";
const env = await initializeTestEnvironment({ projectId: "demo-codebay", firestore: { rules: readFileSync("firestore.rules", "utf8"), host: "127.0.0.1", port: 8085 } });
let pass = 0, fail = 0;
const t = async (name, fn) => { try { await fn(); pass++; console.log("ok  ", name); } catch (e) { fail++; console.log("FAIL", name, "-", e.message.split("\n")[0]); } };
const db = uid => (uid ? env.authenticatedContext(uid) : env.unauthenticatedContext()).firestore();
const lotData = (over = {}) => ({ sellerUid: "sam", sellerName: "Sam", title: "Snake game", desc: "Classic", lang: "python", files: [{ n: "main.py", b: 10 }],
  startBid: 500, endsAt: Timestamp.fromMillis(Date.now() + 3 * 86400000), created: serverTimestamp(), topBid: 0, topUid: "", topName: "", bidCount: 0, status: "live", released: false, ...over });
async function list(uid, id, over = {}, vault = true) { const d = db(uid), b = writeBatch(d);
  b.set(doc(d, "auctions", id), lotData(over)); if (vault) b.set(doc(d, "auctions", id, "vault", "files"), { json: '{"main.py":"print(1)"}' }); return b.commit(); }
async function bid(uid, id, amount, n, opts = {}) { const d = db(uid), b = writeBatch(d);
  b.update(doc(d, "auctions", id), { topBid: amount, topUid: opts.as || uid, topName: "N" + uid, bidCount: n });
  if (!opts.noBidDoc) b.set(doc(d, "auctions", id, "bids", String(opts.docN ?? n)), { uid, name: "N" + uid, amount: opts.docAmount ?? amount, at: serverTimestamp() });
  return b.commit(); }
const admin = async fn => env.withSecurityRulesDisabled(c => fn(c.firestore()));
await env.clearFirestore();

await t("seller lists a lot with its vault", () => assertSucceeds(list("sam", "a1")));
await t("listing without a vault is refused", () => assertFails(list("sam", "a2", {}, false)));
await t("listing for someone else is refused", () => assertFails(list("eve", "a3")));
await t("listing that ends in 10 minutes is refused", () => assertFails(list("sam", "a4", { endsAt: Timestamp.fromMillis(Date.now() + 600000) })));
await t("listing with a pre-set top bid is refused", () => assertFails(list("sam", "a5", { topBid: 900, bidCount: 1, topUid: "sam" })));
await t("listing with an extra field is refused", () => assertFails(list("sam", "a6", { featured: true })));
await t("starting price under $1 is refused", () => assertFails(list("sam", "a7", { startBid: 50 })));
await t("anyone, signed out, can read a lot", () => assertSucceeds(getDoc(doc(db(null), "auctions", "a1"))));
await t("vault can't be added to an existing lot", () => assertFails(setDoc(doc(db("sam"), "auctions", "a1", "vault", "files"), { json: "{}" })));

await t("first bid below the starting price is refused", () => assertFails(bid("ann", "a1", 400, 1)));
await t("signed-out bid is refused", () => assertFails(bid(null, "a1", 500, 1)));
await t("seller can't bid on their own lot", () => assertFails(bid("sam", "a1", 500, 1)));
await t("bid without its bid record is refused", () => assertFails(bid("ann", "a1", 500, 1, { noBidDoc: true })));
await t("bid record with a different amount is refused", () => assertFails(bid("ann", "a1", 500, 1, { docAmount: 99999 })));
await t("bid naming someone else as top bidder is refused", () => assertFails(bid("ann", "a1", 500, 1, { as: "bob" })));
await t("bid that skips the count is refused", () => assertFails(bid("ann", "a1", 500, 2)));
await t("first bid at the starting price is accepted", () => assertSucceeds(bid("ann", "a1", 500, 1)));
await t("the top bidder can't bid against themselves", () => assertFails(bid("ann", "a1", 700, 2)));
await t("raise of less than $1 is refused", () => assertFails(bid("bob", "a1", 550, 2)));
await t("raise of $1 is accepted", () => assertSucceeds(bid("bob", "a1", 600, 2)));
await t("a bid record can't be rewritten", () => assertFails(setDoc(doc(db("bob"), "auctions", "a1", "bids", "2"), { uid: "bob", name: "Nbob", amount: 1, at: serverTimestamp() })));
await t("bidder can't edit the title", () => assertFails(updateDoc(doc(db("ann"), "auctions", "a1"), { title: "Mine now" })));
await t("seller can't withdraw once there are bids", () => assertFails(updateDoc(doc(db("sam"), "auctions", "a1"), { status: "cancelled" })));
await t("seller can't release before the end", () => assertFails(updateDoc(doc(db("sam"), "auctions", "a1"), { released: true })));
await t("seller can read their vault", () => assertSucceeds(getDoc(doc(db("sam"), "auctions", "a1", "vault", "files"))));
await t("top bidder can't read the vault before release", () => assertFails(getDoc(doc(db("bob"), "auctions", "a1", "vault", "files"))));
await t("deal thread is closed while live", () => assertFails(addDoc(collection(db("bob"), "auctions", "a1", "deal"), { uid: "bob", name: "Nbob", text: "hi", at: serverTimestamp() })));
await t("anyone can read the bid history", () => assertSucceeds(getDocs(collection(db(null), "auctions", "a1", "bids"))));

// end the auction
await admin(d => updateDoc(doc(d, "auctions", "a1"), { endsAt: Timestamp.fromMillis(Date.now() - 1000) }));
await t("bid after the end is refused", () => assertFails(bid("ann", "a1", 900, 3)));
await t("winner can post in the deal thread", () => assertSucceeds(addDoc(collection(db("bob"), "auctions", "a1", "deal"), { uid: "bob", name: "Nbob", text: "How do I pay?", at: serverTimestamp() })));
await t("seller can read the deal thread", () => assertSucceeds(getDocs(collection(db("sam"), "auctions", "a1", "deal"))));
await t("outbid bidder can't read the deal thread", () => assertFails(getDocs(collection(db("ann"), "auctions", "a1", "deal"))));
await t("can't post as someone else", () => assertFails(addDoc(collection(db("bob"), "auctions", "a1", "deal"), { uid: "sam", name: "Sam", text: "paid", at: serverTimestamp() })));
await t("winner can't release the files themselves", () => assertFails(updateDoc(doc(db("bob"), "auctions", "a1"), { released: true })));
await t("seller releases after the end", () => assertSucceeds(updateDoc(doc(db("sam"), "auctions", "a1"), { released: true })));
await t("winner reads the vault after release", () => assertSucceeds(getDoc(doc(db("bob"), "auctions", "a1", "vault", "files"))));
await t("outbid bidder still can't read the vault", () => assertFails(getDoc(doc(db("ann"), "auctions", "a1", "vault", "files"))));
await t("seller can't un-release or re-open", () => assertFails(updateDoc(doc(db("sam"), "auctions", "a1"), { released: false })));

await list("sam", "b1");
await t("seller withdraws a lot with no bids", () => assertSucceeds(updateDoc(doc(db("sam"), "auctions", "b1"), { status: "cancelled" })));
await t("nobody can bid on a withdrawn lot", () => assertFails(bid("ann", "b1", 500, 1)));
await t("nobody can delete a lot", () => assertFails(deleteDoc(doc(db("sam"), "auctions", "b1"))));
await t("existing per-user docs still work", () => assertSucceeds(setDoc(doc(db("sam"), "users", "sam", "docs", "v2progress"), { json: "{}", updated: serverTimestamp() })));
await t("other people's docs still locked", () => assertFails(getDoc(doc(db("eve"), "users", "sam", "docs", "v2progress"))));

console.log(`\n${pass} passed, ${fail} failed`);
await env.cleanup(); process.exit(fail ? 1 : 0);
