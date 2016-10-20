// Shield

module shield() {
	intersection() {
	difference() {
	cube([60,10,70]);
	translate([10,15,90])
		rotate([90,0,0])
			cylinder(20,r=35,true,$fn=200);
	translate([50,15,90])
		rotate([90,0,0])
			cylinder(20,r=35,true,$fn=200);		
	}
	translate([60,15,45])
		rotate([90,0,0])
			cylinder(20,r=55,true,$fn=200);
	translate([-2,15,45])
		rotate([90,0,0])
			cylinder(20,r=55,true,$fn=200);
	translate([30,122,0])
		doughnut();
	}
}
module doughnut() {
	difference() {
		cylinder(70,r=119,true,$fn=1000);
		translate([0,0,-5])
		cylinder(80,r=115,true,$fn=1000);
		
	}
}

color([0.8,0.8,0.8]) shield();
