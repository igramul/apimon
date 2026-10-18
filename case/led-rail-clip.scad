LED_inc = 16.667;
LED_w = 10;

module Clip() {
    difference() {
        union() {
            translate([-LED_w/2, -LED_inc/2, 0])
                cube([LED_w, LED_inc, 1.6]);

            translate([0, -1.161, -3.16855])
                rotate([-90,0, 0])
                    import("LED_Strip_Clip-On_Diffuser_Clip.stl", convexity=3);
        }
        translate([-LED_w/2, -LED_inc/2, 1.1])
            cube([LED_w, LED_inc, 0.5]);
    }
}

// Modul: Erzeugt eine Clip-Schiene für n LEDs
module ClipRail(n = 10) {
    union() {
        for (i = [0 : n-1]) {
            translate([0, i * LED_inc, 0])
                Clip();
        }
    }
}

ClipRail(10);
