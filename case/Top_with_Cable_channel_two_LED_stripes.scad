$fn=100;

import("PiZeroCase_Top_NoLogo_NoChamfer_Pins.STL");



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

//cube([240, 33.592, 2], center=true);
//cube([68.584, 33.592, 2], center=true);
//cube([68.584, 24.4, 2.2], center=true);

difference() {
    Platte(x=240+2*r, y=24.38, h=8);
    Platte(x=68.57, y=24.38, h=8);
    translate([0,0, 3.66]) Platte(x=68.97, y=24.78, h=8);
    translate([0,0,6.7]) cube([240, 20, 8], center=true);
    translate([115,20,7]) cube([10, 20, 2], center=true);
    translate([-115,20,7]) cube([10, 20, 2], center=true);
    translate([0,-7.5,7]) cube([260, 5, 3], center=true);
    }


