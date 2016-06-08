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
    hull() {
    translate([-20,0,0]) 
    rotate([0,90,0])
    cylinder(2,r=10,true,$fn=100);
    translate([0,0,-8]) 
    cylinder(16,r=10,true,$fn=100);
    translate([20,0,0]) 
    rotate([0,90,0])
    cylinder(2,r=10,true,$fn=100);
    }
}

module body() {
    hull() {
        translate([0,0,45])
        shoulder();
        base();
    }
}

module head() {
translate([0,0,55])
    difference() {
    cylinder(32,r=15,r2=14,true,$fn=200);
    //Eye slot
    translate([0,-20,5])
        cube([2,10,20]);
    translate([-6.5,-20,23])
        cube([15,10,2]);
    }
}

module arm() {
    difference() {
        translate([-22,0,45]) {
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
        translate([-22,-40,0])
            cube([20,100,100]);
    }
}
module sword() {
    translate([-22,-35,25]) {
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
    
}

module knight() {
    rotate([0,3,0])
        arm();
    sword();
    mirror([1,0,0]) 
        rotate([0,3,0])
            arm();
    head();
    body();
    translate([-12,0,-40])
        leg();
    translate([12,0,-40])
        leg();
}

color([0.8,0.8,0.8]) knight();

