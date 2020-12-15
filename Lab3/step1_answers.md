# Q1:
Dynamic power = power consumed from transistor switching (influenced by the running program)
Leakage = power consumption due to leakage currents on transistors, is there no matter what as
static power (at idle). More of a concern with shrinking transistor sizes. [1]

Dynamic power is what gets affected by the program, depending on what and how many
parts of the CPU the program exerts.

No, dynamic power is solely dependent on the transistor gate capacitance, supply voltage and
switching frequency [2]. Execution time matters on the total **energy** consumption in joules.
Obviously, more time => more **energy, not power**, consumed.

# Q2:
Yes, depending on static power (leakage), dynamic power and execution time. If the 40W processor
consumes 39.9W as dynamic power and 0.1W as leakage, while the 4W processor is 2W leakage and 2W
dynamic, then the 40W wins, under the condition that the program can run faster than on
the 4W one. Otherwise, the 4W one might be more efficient.
Therefore, McPAT's data are not enough to determine energy efficiency, since we need
data dependent on the program under execution (specifically execution time).
Such data can be found by using McPAT together with a simulator like gem5 for the same program.

# Q3:
(append McPAT data here too)
Total leakage power of the Xeon is 100 times bigger than the ARM one, which means that Xeon
will always consume way more power when idle than A9, no matter how faster Xeon is 
(since we suppose that system continues running even after the program is completed, in
which case it would be idle)

[1]: https://en.wikipedia.org/wiki/Processor_power_dissipation (REPLACE THE WIKI SOURCE WITH PROPER ONE)
[2]: https://web.archive.org/web/20150812030010/http://download.intel.com/design/network/papers/30117401.pdf