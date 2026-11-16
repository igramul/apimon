LED_inc = 16.667;
LED_w = 10;

// expand Dome element with connector
module DomeElement() {
    width_factor = 0.6;
    union() {
        translate([-LED_w/2, -LED_inc/2, 0])
        difference() {
            cube([LED_w, LED_inc, 1.6]);
            translate([0, (LED_inc-width_factor*LED_inc)/2, 0])
                cube([LED_w, width_factor*LED_inc, 1.6]);
        }
        import("LED_Strip_Clip-On_Diffuser_Dome.stl", convexity=3);
    }
}

// Modul: render a Dome rail for n LEDs
module DomeRail(n = 10) {
    union() {
        for (i = [0 : n-1]) {
            translate([0, i * LED_inc, 0])
                DomeElement();
        }
    }
}

DomeRail(10);
