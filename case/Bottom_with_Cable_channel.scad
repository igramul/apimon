// cut some cable canels

difference() {
import("PiZeroCase_Bottom_NoChamfer.STL");

// pin header cut
translate([10.5,-11.5,0])
cube([31,5,5], center=true);

// channel for LED stripe cable
translate([0,-16,0])
cube([11,14,4], center=true);

// connection channel
translate([23.5,-1.5,-1])
cube([5,20,4], center=true);

// channel for power inlet
translate([35.74,6,0])
cube([20,5,4], center=true);   
}