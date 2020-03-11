# Examples

In this directory are some examples of the config file and some scripts you could use to make cron work well with this program when using a virtual environment. 

If using the example.config.json file, rename it to config.json and put it in $HOME/.config/snapintime (or /root/.config/snapintime/ if you’re going to run as root.

For information on how to edit the config, see: https://snap-in-time.readthedocs.io/en/latest/config.html

I recommend that if you use PyPi to install snapintime, that you run it in a virtual environment. If so, cron might have issues. So I have some bash files you can use as examples. Replace the "cd" line with the directory you've installed snapintime into. I recommend splitting it up this way so you have control over how often you're running each part of the script. I have some explanations of my justifications here: https://snap-in-time.readthedocs.io/en/latest/usage.html
