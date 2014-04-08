Command to run
python astar.py -X startX -Y startY -x endX -y endY map.txt
Start and End coordinates are on a 0 count system. Max start/end X/Y values is the dimensions of the map-1. If the map is 10x10, the coordinates should not exceed 9.

Example: python astar.py -X 2 -Y 3 -x 4 -y 5 map.txt
The start block will appear in the 3rd column and 4th row. The end block will appear in the 5th column and 6th row.

If values on each box becomes problamatic in large maps, add the argument "big" at the end of the command to remove font. The screen may not be large enough to view entire map though.
Example: python astar.py -X 2 -Y 3 -x 4 -y 5 map.txt big

To change the speed, press the up and down arrows to make the animation quicker(up arrow) or slower(down arrow).