/// @description Insert description here
// You can write your code in this editor
//get player input

if (hascontrol)
{
key_left = keyboard_check(vk_left) || keyboard_check(ord("A"));
key_right = keyboard_check(vk_right) || keyboard_check(ord("D"));
key_jump = keyboard_check(vk_space) 

}
else
{
	key_right = 0;
	key_left = 0;
	key_jump = 0;
}	

//calc movement
var move = key_right - key_left;

hsp = (move*walksp)+gunkickx;
gunkickx = 0;
vsp = (vsp+grv)+gunkicky;
gunkicky = 0;

if (place_meeting(x,y+1,oWall)) && (key_jump)
{
	vsp = -7;
}

//horiz collision
if (place_meeting(x+hsp,y,oWall))
{
	while (!place_meeting(x+sign(hsp),y,oWall))
	{
		x = x + sign(hsp);
	}
	hsp = 0;
}
x = x + hsp;

//vert collision
if (place_meeting(x,y+vsp,oWall))
{
	while (!place_meeting(x,y+sign(vsp),oWall))
	{
		y = y + sign(vsp);
	}
	vsp = 0;
}
y = y + vsp;

//animation
if (!place_meeting(x,y+1,oWall))
{
	sprite_index = SpriteJump;
	image_speed = 0;
	if (sign(vsp) > 0) image_index = 1; else image_index = 0;
}
else
{
	image_speed=1;
	if (hsp == 0)
	{
		sprite_index = SpriteIdle;
	}
	else
	{
		sprite_index = SpriteRun;
	}
}

if (hsp != 0) image_xscale = sign(hsp);