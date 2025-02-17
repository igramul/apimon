// cut some cable canels

difference() {
import("PiZeroCase_Bottom_NoChamfer.STL");


translate([0,-11.5,0])
cube([52,4,5], center=true);

translate([0,-15,-1])
cube([8,4,4], center=true);

translate([20,5,-1])
cube([4,30,4], center=true);

}