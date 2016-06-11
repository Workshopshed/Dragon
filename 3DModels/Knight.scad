// Knight Model
use <SG90.scad>;

module shoe() {
    scale([1,1,1.2])
    difference(){
        rotate([0,45,0])
            hull() {
            cube([5,0.2,5], true);
            translate([0,25,0])
                rotate([0,90,90])
                    cylinder(0.2,r=8,true,$fn=200);
        }
        //Slice off bottom
        translate([0,15,-5])
            cube([20,35,10],true);
        //Tiedown
        translate([0,10,-1])
            cylinder(6,r=1,true,$fn=200);
        }
}

module leg() {
    difference(){
        union(){
        cylinder(50,r=6,r2=9,true,$fn=200);
        translate([0,0,26])     
        sphere(9.5,true,$fn=200);    
        translate([0,-25,0]) 
        shoe();
        }
        translate([0,0,-2]) 
            cylinder(60,r=4,r2=7,true,$fn=200);
    }
}

module base() {
    hull() {
    translate([-15,0,0]) 
    cylinder(2,r=10,true,$fn=200);
    cylinder(2,r=14,true,$fn=200);
    translate([15,0,0]) 
    cylinder(2,r=10,true,$fn=200);
    }
}

module shoulder() {
	size=14;
	width=23;
    hull() {
    translate([-width,0,0]) 
    rotate([0,90,0])
    cylinder(2,r=size,true,$fn=100);
    translate([0,0,-8]) 
    cylinder(16,r=size+3,true,$fn=100);
    translate([width,0,0]) 
    rotate([0,90,0])
    cylinder(2,r=size,true,$fn=100);
    }
}

module body() {
	difference() {
		hull() {
			translate([0,0,45])
				shoulder();
			base();
		}
		translate([-27,-20,45.5])
			cube([55,42,22]);
		translate([-15.25,-7,23])
			cube([3,14,34]);
		translate([-20,-7,28])
			cube([42,14,24]);
		translate([-30,0,45.5])
			rotate([0,90,0])
				cylinder(30,d=13,true,$fn=100);
		translate([-12,0,-40])
			cylinder(50,r=9.25,true,$fn=200);
		translate([20,0,45.5])
			rotate([0,90,0])
				cylinder(10,d=3,true,$fn=100);
		translate([12,0,-40])
			cylinder(50,r=9.25,true,$fn=200);
		translate([6.5,-7,-40])
			cube([11,14,100]);

	}
}

module body_top() {
	
	difference() {
		union() {
			hull() {
				translate([0,0,45])
					shoulder();
				base();
			}
			translate([0,0,50])
			cylinder(14,d=22,true,$fn=100);
		}	
		translate([-27,-20,-3.5])
			cube([55,42,49]);
		translate([-15.25,-7,23])
			cube([3,14,34]);
		translate([-20,-7,28])
			cube([42,14,24]);
		translate([-30,0,45.5])
			rotate([0,90,0])
				cylinder(30,d=13,true,$fn=100);
		translate([20,0,45.5])
			rotate([0,90,0])
				cylinder(10,d=3,true,$fn=100);
		translate([0,0,45.5])
			cylinder(30,d=11,true,$fn=100);
		translate([15,0,45])
			rotate([0,-55,0])
				cylinder(18,d=11,true,$fn=100);		
	}
}

module head() {
    difference() {
    cylinder(32,r=15,r2=14,true,$fn=200);
    //Eye slot
    translate([0,-20,5])
        cube([2,10,20]);
    translate([-6.5,-15,23])
        cube([15,10,3]);
	//Neck
	translate([0,0,-5])
		cylinder(35,d=23,true,$fn=100);
    }
}

module arm() {
    difference() {
        translate([0,0,45]) {
            sphere(12,true,$fn=200);
            translate([0,0,-23]) {
                cylinder(23,r=9,r2=11,true,$fn=100);
                sphere(10,true,$fn=100);
                translate([0,0,-3]) {
                rotate([90,0,00])
                cylinder(30,r=7,r2=6,true,$fn=100);
                translate([0,-25,0])
                sphere(8,true,$fn=200);
                }
            }
        }
        translate([0,-40,0])
            cube([20,100,100]);
		translate([-15,0,45.25])
			rotate([0,85,0])
				cylinder(20,d=5,true,$fn=100);
		translate([-20,0,45.25])
			rotate([0,85,0])
				cylinder(10,d=8,true,$fn=100);

    }
}
module sword() {
     union() {
        hull() {
            translate([2.5,0,0]) 
            cylinder(5,r=2,true,$fn=200);
            translate([3,10,0]) 
            cylinder(5,r=3,true,$fn=200);
            translate([2.5,20,0]) 
            cylinder(5,r=2,true,$fn=200);
        }
        hull() {
            translate([1.3,4,5]) 
            cylinder(40,r=1,true,$fn=200);
            translate([2,10,5]) 
            cylinder(50,r=2,true,$fn=200);
            translate([1.3,16,5]) 
            cylinder(40,r=1,true,$fn=200);
        }
        translate([0,7,-15])
        cube([5,5,20]);
        translate([0,10,-5])
            difference() {
                sphere(8,true,$fn=100);
                translate([-10,-10,-10])
                    cube([10,20,20]);
            }
	}
    
}

module shield() {
	translate([30,15,29])
	   rotate([0,-5,0])
	   //Hand + handle
       difference() {
		   union() {
			   sphere(8,true,$fn=200);
			   rotate([90,0,0])
				  cylinder(8,r=8,$fn=200);
		   }	   
           translate([0,-10,-10])
                    cube([10,20,20]);
	   }
	intersection() {
	difference() {
	cube([60,10,70]);
	translate([10,15,90])
		rotate([90,0,0])
			cylinder(20,r=35,true,$fn=500);
	translate([50,15,90])
		rotate([90,0,0])
			cylinder(20,r=35,true,$fn=500);		
	}
	translate([60,15,45])
		rotate([90,0,0])
			cylinder(20,r=55,true,$fn=400);
	translate([-2,15,45])
		rotate([90,0,0])
			cylinder(20,r=55,true,$fn=400);
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

module knight() {
	explode=0; //20*$t;
	armpos=28.1;
	translate([-armpos-explode,0,0])
		rotate([0,5,0])
			arm();
	translate([-armpos-(explode/2),-35,24])
		sword();
	translate([armpos+explode,0,0])
		mirror([1,0,0]) 
			rotate([0,5,0])
				arm();
	translate([0,0,59+explode])
		head();
    body();
	translate([0,0,explode/2])
	body_top();
    translate([-12,0,-40-explode])
        leg();
    translate([12,0,-40-explode])
        leg();
	translate([-4+(explode/4),-41-(explode/2),-10])
		shield();
}

color([0.8,0.8,0.8]) knight();

/* Servo to move arm
translate([3,0,40])
	rotate([0,-90,0])
		*sg90();
*/
