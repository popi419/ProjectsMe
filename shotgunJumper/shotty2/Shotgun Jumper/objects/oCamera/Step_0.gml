/// @description Insert description here
// You can write your code in this editor

//update movement
if (instance_exists(follow))
{
	xTo = follow.x;
	yTo = follow.y;
	
	if ((follow).object_index == oPlayerRIP)
	{
		x = xTo;
		y = yTo;
	}
}

//update pos
x += (xTo - x) / 25;
y += (yTo - y) / 25;

x = clamp(x,view_w_half,room_width-view_w_half);
y = clamp(y,view_h_half,room_height-view_h_half);

//update cam
camera_set_view_pos(cam,x-view_w_half,y-view_h_half);