from _lib import *

PATH(id="systems", title="Systems Programmer", icon="binary", hue="#ff8a3d", cat="Systems & Hardware", duration="14–20 months",
 tagline="Write the low-level software everything else runs on: compilers, runtimes, databases, OS.",
 about=["Systems programmers build foundational software: operating systems, compilers, databases, browsers, runtimes and high-performance infrastructure. You'll work close to the hardware in C, C++ or Rust and care about memory, concurrency and every microsecond.","It's demanding and deeply rewarding, and the knowledge makes you a better engineer in any role."],
 day=["Write performance-critical code in Rust, C or C++", "Profile and optimise hot paths", "Debug memory and concurrency bugs", "Design data structures with predictable performance", "Read and contribute to large codebases"],
 tools=["C", "C++", "Rust", "gdb/lldb", "perf", "Valgrind & sanitizers", "LLVM", "Linux"],
 roles=["Systems Engineer", "Compiler Engineer", "Database Engineer", "Kernel Developer", "Performance Engineer"],
 core=["s3m1", "s3m2", "s3m3", "s3m4", "s3m5", "s7m2", "s7m5"],
 phases=[
  PH("How computers work", "Weeks 1–12", "From logic gates to processes.", [
   N("C programming", "Pointers, memory and manual allocation: programming without a safety net.", ["pointers", "malloc & free", "structs", "undefined behaviour"], ["cs50", "learncpp"], core="s3m1"),
   N("Data representation", "Bits, integers, floating point and memory layout.", ["two's complement", "IEEE 754", "endianness", "alignment"], ["nand2tetris"], core="s3m2"),
   N("Computer architecture", "CPUs, instructions, pipelines and caches.", ["assembly basics", "pipelining", "cache hierarchy"], ["nand2tetris"], core="s3m3"),
   N("Operating systems", "Processes, virtual memory, scheduling and file systems.", ["processes & threads", "virtual memory", "scheduling", "system calls"], ["ostep"], core="s3m4"),
  ], ("Build a shell", "Write a Unix shell in C supporting pipes, redirection, background jobs and built-ins, with no memory errors under sanitizers.")),
  PH("Modern systems languages", "Weeks 13–26", "Safety and performance together.", [
   N("Rust", "Ownership and borrowing give memory safety without a garbage collector.", ["ownership & borrowing", "lifetimes", "traits", "error handling"], ["rust-book", "rustlings", "rm-rust"]),
   N("Modern C++", "RAII, smart pointers, templates and move semantics.", ["RAII", "smart pointers", "move semantics", "STL"], ["learncpp", "cppref", "rm-cpp"], opt=True),
   N("Concurrency", "Threads, atomics, memory ordering and lock-free basics.", ["mutexes", "atomics", "memory ordering", "async runtimes"], ["ostep"], core="s3m5"),
   N("Debugging & tooling", "Debuggers, sanitizers and profilers.", ["gdb/lldb", "AddressSanitizer", "perf", "flame graphs"], [("Brendan Gregg: Linux performance", "https://www.brendangregg.com/linuxperf.html")], core="s5m5"),
  ]),
  PH("Deep specialisation", "Months 7–20", "Build one of the classic systems from scratch.", [
   N("Compilers & interpreters", "Lexing, parsing, ASTs, bytecode and code generation.", ["lexers & parsers", "ASTs", "bytecode VMs", "LLVM"], ["crafting", "llvm"], core="s7m2"),
   N("Databases internals", "Storage engines, indexes, query execution and transactions.", ["B-trees & LSM trees", "buffer pools", "query execution", "MVCC"], ["cmu-db"], core="s7m5"),
   N("Networking stacks", "Sockets, event loops and high-performance servers.", ["sockets", "epoll/io_uring", "protocol parsing"], ["beej-net"]),
   N("Performance engineering", "Data-oriented design, SIMD and cache-aware code.", ["cache-friendly layouts", "SIMD", "benchmarking"], ["teachyourself"], core="s7m5"),
   N("Distributed systems", "Replication, consensus and fault tolerance.", ["Raft", "replication", "consistency models"], [("MIT 6.5840 Distributed Systems", "https://pdos.csail.mit.edu/6.824/")], core="s6m3"),
  ], ("Build a classic", "Implement one of: an interpreter for a small language, a key-value store with a write-ahead log, or a Raft-replicated log. Benchmark it and write up the design.")),
 ],
 interview=["Pointers, memory layout and undefined behaviour.", "Concurrency: implement a thread-safe queue.", "Explain virtual memory, caches and what makes code fast.", "Deep dive into a systems project you built."],
 related=["embedded", "backend", "game-dev"])

PATH(id="embedded", title="Embedded & IoT Engineer", icon="board", hue="#38d3f0", cat="Systems & Hardware", duration="12–16 months",
 tagline="Program the tiny computers inside cars, medical devices, wearables and smart homes.",
 about=["Embedded engineers write software for microcontrollers and devices with tight limits on memory, power and timing. You'll read datasheets, talk to sensors over hardware buses, write firmware in C or Rust and debug with oscilloscopes as well as debuggers.","Start with an inexpensive development board; seeing an LED blink because of your code never gets old."],
 day=["Write firmware in C or Rust", "Bring up new hardware and drivers", "Talk to sensors over I2C, SPI and UART", "Debug timing and power issues", "Implement connectivity and over-the-air updates"],
 tools=["C", "Rust", "Arduino", "ESP32", "STM32", "FreeRTOS / Zephyr", "Logic analyser", "Oscilloscope", "JTAG/SWD debugger"],
 roles=["Embedded Software Engineer", "Firmware Engineer", "IoT Engineer", "Embedded Linux Engineer"],
 core=["s3m1", "s3m2", "s3m3", "s3m4"],
 phases=[
  PH("C & electronics basics", "Weeks 1–10", "Code and circuits.", [
   N("C for embedded", "Pointers, bit manipulation, volatile and fixed-width integers.", ["pointers", "bitwise operations", "volatile", "stdint types"], ["cs50", "learncpp"], core="s3m1"),
   N("Electronics fundamentals", "Voltage, current, resistance and reading a schematic.", ["Ohm's law", "digital vs analog", "pull-up resistors", "schematics"], [("SparkFun tutorials", "https://learn.sparkfun.com/tutorials")]),
   N("Your first microcontroller", "Blink an LED, read a button, print over serial.", ["GPIO", "serial output", "Arduino IDE"], ["arduino"]),
   N("Binary & hardware registers", "Configure hardware by setting bits in memory-mapped registers.", ["memory-mapped I/O", "register maps", "datasheets"], ["nand2tetris"], core="s3m2"),
  ], ("Sensor station", "A microcontroller reading temperature and light sensors, displaying values on a small screen and logging them over serial.")),
  PH("Firmware engineering", "Weeks 11–26", "Write reliable firmware on real microcontrollers.", [
   N("Communication protocols", "How chips talk to each other.", ["UART", "I2C", "SPI", "CAN"], [("SparkFun tutorials", "https://learn.sparkfun.com/tutorials")]),
   N("Interrupts & timers", "Respond to events instantly and keep precise time.", ["ISRs", "timers", "PWM", "debouncing"], ["arduino"]),
   N("Real-time operating systems", "Tasks, scheduling and synchronisation with an RTOS.", ["tasks", "priorities", "queues & semaphores", "deadlines"], ["freertos", "zephyr"], core="s3m4"),
   N("Low-power design", "Make batteries last months instead of days.", ["sleep modes", "power budgets", "measuring current"], ["zephyr"]),
   N("Debugging hardware", "Debuggers, logic analysers and oscilloscopes.", ["JTAG/SWD", "logic analyser", "oscilloscope basics"], ["zephyr"]),
   N("Embedded Rust", "Memory-safe firmware.", ["no_std", "HALs", "embedded-hal"], ["embedded-rust"], opt=True),
  ], ("RTOS-based device", "Firmware with multiple RTOS tasks (sensing, display, logging) communicating through queues, with low-power sleep between readings.")),
  PH("Connected devices", "Months 7–16", "IoT, Linux and production concerns.", [
   N("Wireless & IoT protocols", "Wi-Fi, Bluetooth Low Energy and MQTT.", ["BLE", "Wi-Fi", "MQTT", "LoRa"], [("MQTT.org", "https://mqtt.org/")]),
   N("Embedded Linux", "Linux on single-board computers and custom images.", ["Raspberry Pi", "device trees", "Yocto/Buildroot basics"], ["rpi"], opt=True),
   N("Device security", "Secure boot, encrypted communication and safe updates.", ["secure boot", "TLS on devices", "signed OTA updates"], ["owasp-cs"]),
   N("Testing firmware", "Unit tests on the host, hardware-in-the-loop tests.", ["unit testing C", "mocks", "HIL testing"], ["zephyr"]),
  ], ("IoT product prototype", "A battery-powered device that sends sensor data over MQTT to a dashboard, supports secure over-the-air updates and runs for a week on one charge.")),
 ],
 interview=["C questions: pointers, volatile, bit manipulation.", "Explain interrupts and race conditions in ISRs.", "Protocol questions: I2C vs SPI vs UART.", "Debugging scenario on real hardware."],
 related=["systems", "robotics"])

PATH(id="robotics", title="Robotics Software Engineer", icon="robot", hue="#a3e635", cat="Systems & Hardware", duration="16–24 months",
 tagline="Make machines perceive, plan and move in the real world.",
 about=["Robotics software engineers write the code that lets robots sense their surroundings, decide what to do and act safely: perception, localisation, planning and control. The field blends programming, maths, physics and machine learning.","Simulation lets you learn most of it without buying hardware, and ROS 2 is the industry's common toolkit."],
 day=["Develop perception from cameras and lidar", "Implement localisation and mapping", "Plan paths and motions", "Tune controllers on real hardware", "Test in simulation before deploying"],
 tools=["C++", "Python", "ROS 2", "Gazebo", "OpenCV", "PyTorch", "Linux", "Eigen"],
 roles=["Robotics Software Engineer", "Perception Engineer", "Motion Planning Engineer", "Controls Engineer"],
 core=["s1m6", "s2m5", "s3m5", "s7m3"],
 phases=[
  foundations("Python"),
  PH("Maths & physics for robots", "Weeks 9–20", "The language robots are described in.", [
   N("Linear algebra & transforms", "Rotations, homogeneous transforms and coordinate frames.", ["matrices", "rotations & quaternions", "coordinate frames"], ["3b1b-la"]),
   N("Probability for robotics", "Robots are never certain where they are.", ["Bayes filters", "Gaussian distributions", "sensor noise"], ["seeing"]),
   N("Kinematics", "How joints and wheels map to motion.", ["forward kinematics", "inverse kinematics", "differential drive"], [("Modern Robotics (free textbook and videos)", "https://hades.mech.northwestern.edu/index.php/Modern_Robotics")]),
   N("Control theory", "Make systems follow a target smoothly.", ["feedback", "PID control", "stability"], [("Modern Robotics (free textbook and videos)", "https://hades.mech.northwestern.edu/index.php/Modern_Robotics")]),
  ]),
  PH("ROS 2 & simulation", "Weeks 21–34", "The standard robotics software stack.", [
   N("ROS 2 fundamentals", "Nodes, topics, services, actions and launch files.", ["nodes & topics", "services & actions", "launch files", "tf2"], ["ros2"]),
   N("Simulation", "Test robots safely in Gazebo before touching hardware.", ["URDF models", "Gazebo", "sensor simulation"], ["ros2"]),
   N("C++ for robotics", "Performance-critical robot code.", ["modern C++", "Eigen", "real-time constraints"], ["learncpp"]),
   N("Computer vision", "Detect and track objects with cameras.", ["OpenCV", "camera calibration", "feature detection", "deep-learning detectors"], ["opencv", "cs231n"]),
  ], ("Simulated mobile robot", "A ROS 2 robot in Gazebo that maps a room, localises itself and drives to goals while avoiding obstacles.")),
  PH("Autonomy", "Months 9–24", "Perception, planning and learning together.", [
   N("Localisation & SLAM", "Estimate position and build maps at the same time.", ["Kalman filters", "particle filters", "SLAM"], ["ros2"]),
   N("Motion planning", "Find safe, efficient paths for robots and arms.", ["A* & D*", "sampling planners (RRT)", "trajectory optimisation"], ["redblob", "ros2"], core="s2m5"),
   N("Robot learning", "Learn behaviours from data and simulation.", ["imitation learning", "reinforcement learning basics", "sim-to-real"], ["pytorch", ("Hugging Face Deep RL course", "https://huggingface.co/learn/deep-rl-course")], opt=True),
   N("Safety & testing", "Robots move in the physical world; failures matter.", ["safety cases", "simulation testing", "fail-safe states"], ["ros2"]),
  ], ("Pick-and-place or navigation stack", "A complete autonomy demo (simulated arm picking objects using vision, or a mobile robot navigating a building) with a video and technical write-up.")),
 ],
 interview=["Transforms, rotations and kinematics questions.", "Implement a filter or planner (for example A*).", "C++ fundamentals and performance.", "Explain a robotics project in depth, including what failed."],
 related=["embedded", "ml-engineer", "systems"])
