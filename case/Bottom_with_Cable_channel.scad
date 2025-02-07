// cut the cable channels

// polygon
points = [
    [17, 8],
    [35, 8],
    [35, 3],
    [26, 3],
    [26, -14],
    [5.5, -14],
    [5.5, -18],
    [-5.5, -18],
    [-5.5, -9],
];

difference() {
import("PiZeroCase_Bottom_NoChamfer.STL");

// polygon
translate([0,0,-2])
linear_extrude(height = 4) {
    polygon(points);
}

}