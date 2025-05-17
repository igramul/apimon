// cut the cable cannels

// polygon
points = [
    [-26, -14],
    [26, -14],
    [26, -8],
    [29, -5],
    [40, -5],
    [40, 5],
    [-40, 5],
    [-40, -5],
    [-29, -5],
    [-26, -8],
];


difference() {
    import("PiZeroCase_Bottom_NoChamfer.STL");
    
    // polygon
    translate([0,0,-2])
    linear_extrude(height = 4) {
        polygon(points);
    }    
}

