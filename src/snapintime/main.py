import argparse

def main():
    parser = argparse.ArgumentParser(
            prog="snapintime",
            description="Create btrfs snapshots, cull them over time, and back them up to a server",
            epilog="")
    parser.add_argument('-m', "--mode", choices=["snapshot", "cull", "remote_backup", "remote_cull"], required=True)
    args = parser.parse_args()
    match args.mode:
        case "snapshot":
            print("snapshot")
        case "cull":
            print("cull")
        case "remote_backup":
            print("remote_backup")
        case "remote_cull":
            print("remote_cull")


