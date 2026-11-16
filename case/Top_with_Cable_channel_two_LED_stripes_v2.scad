$fn=100;

module PiZeroCase_Top() {
    import("PiZeroCase_Top_NoLogo_NoChamfer_Pins.STL");
}

use <led-rail-clip.scad>

r=4.6;
yt=12.19;
h=2;

module Platte(x,y,h) {
    translate([0,0,h/2])
    hull(){
        translate([x/2-r, y/2, 0]) cylinder(r=4.6, h=h, center=true);
        translate([x/2-r, -y/2, 0]) cylinder(r=4.6, h=h, center=true);
        translate([-x/2+r, y/2, 0]) cylinder(r=4.6, h=h, center=true);
        translate([-x/2+r, -y/2, 0]) cylinder(r=4.6, h=h, center=true);
    }
}

module TopWithCableChannel() {
    difference() {
        union() {
            translate([0, 0, -0.5]) Platte(x=240+2*r, y=24.38, h=8.5);
            translate([115, 25.12, 8]) rotate([0, 180, 0]) ClipRail(10);
            translate([-115, 25.12, 8]) rotate([0, 180, 0]) ClipRail(10);
        }
        Platte(x=68.57, y=24.38, h=8);
        translate([0,0, 3.66]) Platte(x=68.97, y=24.78, h=8);
        translate([0,0,6.7]) cube([240, 20, 8], center=true);
        translate([115,10,4.9]) cube([10, 20, 4], center=true);
        translate([-115,10,4.9]) cube([10, 20, 4], center=true);
        translate([0,-7.5,5.4]) cube([260, 5, 3], center=true);
    }
}

module ClipRailMask() {
    translate([40, -20, 3.9]) cube([100, 205, 10]);
    translate([-140, -20, 3.9]) cube([100, 205, 10]);
}

module ClipRailMaskNegtive() {
    difference() {
        cube([400, 400, 20], center=true);
        ClipRailMask();
    }
}

// drei Teile können erstellt werden:
TOP_PART = 0;
BOTTOM_LEFT = 1;
BOTTOM_RIGHT = 2;

// Welcher Part soll dargestellt / gerendert werden:
part_index = BOTTOM_RIGHT;


if (part_index == TOP_PART) {
    // ohne ClipRails
    PiZeroCase_Top();
    difference() {TopWithCableChannel(); ClipRailMask(); }

} else if (part_index == BOTTOM_LEFT) {
    // nur die Teile mit den CLipRails (links)
    difference() {
        TopWithCableChannel();
        ClipRailMaskNegtive();
        translate([-100, 0, 0]) cube([200, 400, 20], center=true);
    }
} else if (part_index == BOTTOM_RIGHT) {
    // nur die Teile mit den CLipRails (rechts)
    difference() {
        TopWithCableChannel();
        ClipRailMaskNegtive();
        translate([100, 0, 0]) cube([200, 400, 20], center=true);
    }
} else {
    echo(str("Error: wrong part_index <", part_index, ">"));
    echo(unknown);
}