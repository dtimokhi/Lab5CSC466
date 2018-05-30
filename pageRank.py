import pageRank_support as ps
import sys

def main():
    filename = sys.argv[1]
    snap = eval(sys.argv[2])
    ps.run_page_rank(filename,.15,.001, snap)

    print("")
    print("Nodes ranked in descending order are in ranks.txt")

if __name__ == "__main__":
    main()