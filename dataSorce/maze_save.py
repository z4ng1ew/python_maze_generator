class MazeSave:
    def save(self, size, right_walls, bottom_walls):
        with open(f"./dataSorce/save_mazes/{size}-{size}.txt", "w") as f:

            f.write(f"{size} {size}\n")

            for row in right_walls:
                f.write(" ".join(map(str, row)) + "\n")

            f.write("\n")

            for row in bottom_walls:
                f.write(" ".join(map(str, row)) + "\n")
            
            print("файл создан!!")
        