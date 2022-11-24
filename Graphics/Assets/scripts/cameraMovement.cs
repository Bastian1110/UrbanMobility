using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraMovement : MonoBehaviour
{
    public float x,y,speed = 2.5f;

    private Vector3 rotate; 
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKey(KeyCode.RightArrow))
     {
         transform.Translate(new Vector3(speed * Time.deltaTime,0,0));
     }
     if(Input.GetKey(KeyCode.LeftArrow))
     {
         transform.Translate(new Vector3(-speed * Time.deltaTime,0,0));
     }
     if(Input.GetKey(KeyCode.A))
     {
         transform.Translate(new Vector3(0,-speed * Time.deltaTime,0));
     }
     if(Input.GetKey(KeyCode.S))
     {
         transform.Translate(new Vector3(0,speed * Time.deltaTime,0));
     }
     if(Input.GetKey(KeyCode.UpArrow))
     {
        transform.Translate(new Vector3(0,0,speed * Time.deltaTime));
     }
     if(Input.GetKey(KeyCode.DownArrow))
     {
        transform.Translate(new Vector3(0,0,-speed * Time.deltaTime));
     }

    x = Input.GetAxis("Mouse X");
    y = Input.GetAxis("Mouse Y");

    rotate = new Vector3 (y, x * -1, 0);
    transform.eulerAngles = transform.eulerAngles - rotate;

    transform.eulerAngles += rotate * speed;


    }
}
