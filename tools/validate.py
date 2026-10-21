import json,sys,re
def check(path):
    d=json.load(open(path)); errs=[]; ids=set()
    def uid(i):
        if i in ids: errs.append("dup id "+i)
        ids.add(i)
    def q(x,ctx):
        uid(x.get("id","?"))
        for k in ("id","level","type","prompt","explain"):
            if k not in x: errs.append(f"{ctx}: missing {k}")
        t=x.get("type")
        if t=="mcq":
            if not isinstance(x.get("answer"),int) or not (0<=x["answer"]<len(x.get("options",[]))): errs.append(f"{ctx}: bad mcq answer")
        elif t=="predict":
            if not isinstance(x.get("answer"),str): errs.append(f"{ctx}: predict answer not str")
        elif t=="parsons":
            L=x.get("lines",[])
            if len(L)<3 or len(set(L))!=len(L): errs.append(f"{ctx}: parsons lines <3 or duplicates")
        else: errs.append(f"{ctx}: bad type {t}")
        if x.get("level") not in (1,2,3): errs.append(f"{ctx}: bad level")
    for m in d["modules"]:
        uid(m["id"])
        for k in ("title","summary","lessons","project","exam"):
            if k not in m: errs.append(f"{m['id']}: missing {k}")
        for l in m["lessons"]:
            uid(l["id"])
            for k in ("title","objective","concept","tryit","questions"):
                if k not in l: errs.append(f"{l['id']}: missing {k}")
            v=l.get("visual")
            if v:
                if v.get("type") not in ("steps","compare","table","trace","boxes"): errs.append(f"{l['id']}: bad visual")
                if v.get("type")=="trace":
                    n=len(v["code"].split("\n"))
                    for s in v["steps"]:
                        if not (1<=s["line"]<=n): errs.append(f"{l['id']}: trace line out of range")
            lv={x.get("level") for x in l["questions"]}
            if not {1,2,3}<=lv: errs.append(f"{l['id']}: missing a level")
            for x in l["questions"]: q(x,l["id"])
        for x in m["exam"]: q(x,m["id"]+" exam")
    nl=sum(len(m["lessons"]) for m in d["modules"]); nq=len([i for i in ids if re.search(r"(q|e)\d+$",i)])
    print(f"{path}: {len(d['modules'])} modules, {nl} lessons, {nq} questions, {len(errs)} errors")
    for e in errs[:40]: print("  ",e)
    return not errs
ok=all([check(p) for p in sys.argv[1:]]); sys.exit(0 if ok else 1)
