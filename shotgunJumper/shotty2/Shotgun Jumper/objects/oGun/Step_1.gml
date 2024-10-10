/// @description Insert description here
// You can write your code in this editor
x = oPlayer.x+4;
y = oPlayer.y-8;

image_angle = point_direction(x,y,mouse_x,mouse_y);

firingdelay = firingdelay -1;
recoil = max(0,recoil - 1); 
if (mouse_check_button(mb_left)) && (firingdelay < 0)
{
	
	recoil = 25;
	firingdelay = 50;
	with (instance_create_layer(x,y,"bullet",oBullet))
	{
		speed = 25;
		direction = other.image_angle + random_range(-3,3);
		image_angle = direction;
	}
	
	with (oPlayer)
	{
		gunkickx = lengthdir_x(100, other.image_angle-180);
		gunkicky = lengthdir_y(10, other.image_angle-180);
	}


}

x = x - lengthdir_x(recoil,image_angle);
y = y - lengthdir_y(recoil,image_angle);

if (image_angle > 90) && (image_angle < 270)
{
	image_yscale = -1;	
}
else
{
	image_yscale = 1;
}

