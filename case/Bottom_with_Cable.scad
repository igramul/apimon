// cut some cable canels

difference() {
import("PiZeroCase_Bottom_NoChamfer.STL");


translate([0,-11.5,0])
cube([52,4,5], center=true);

translate([0,-15,-1])
cube([11,4,4], center=true);

translate([24,-2,-1])
cube([4,20,4], center=true);

translate([30,6,-1])
cube([10,4,4], center=true);

}