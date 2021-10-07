/// <summary>
/// write by 52cwalk,if you have some question ,please contract lycwalk@gmail.com
/// </summary>

using UnityEngine;
using System;
using UnityEngine.UI;
using TMPro;
using ZXing;


public class QRCodeDecodeController : MonoBehaviour
{
	public delegate void QRScanFinished(string str);  //declare a delegate to deal with the QRcode decode complete
	public event QRScanFinished onQRScanFinished;  		//declare a event with the delegate to trigger the complete event
    bool sc=false;
	
	bool decoding = false;		
	bool tempDecodeing = false;
	static string dataText = null;
	public DeviceCameraController e_DeviceController = null; 
	private Color[] orginalc;   	//the colors of the camera data.
	private Color32[] targetColorARR;   	//the colors of the camera data.
	private byte[] targetbyte;		//the pixels of the camera image.
	private int W, H, WxH;			//width/height of the camera image
	int byteIndex = 0;				
	int framerate = 0;

    private InputField input, correo, pass, seleccion;
    private GameObject imageerror;
    private TextMeshProUGUI texterror;
    private GameObject p1, p2, p3;
  

	#if UNITY_IOS
	int blockWidth = 450;
	#elif UNITY_ANDROID
	int blockWidth = 350;
	#else
	int blockWidth = 350;
	#endif
	bool isInit = false;
	BarcodeReader barReader;
	void Start()
	{
        input = GameObject.Find("Canvas/Panel2/serial").GetComponent<InputField>();
        seleccion = GameObject.Find("Canvas/Panel2/seleccion").GetComponent<InputField>();
        correo = GameObject.Find("Canvas/Panel/correo").GetComponent<InputField>();
        pass = GameObject.Find("Canvas/Panel/pass").GetComponent<InputField>();
        p1 = GameObject.Find("Canvas/Panel");
        p2 = GameObject.Find("Canvas/Panel2");
        p3 = GameObject.Find("Canvas/Panel3");
        imageerror = GameObject.Find("Canvas/Panel/error");
        texterror = GameObject.Find("Canvas/Panel/error/text").GetComponent<TextMeshProUGUI>();
        Debug.Log(correo.name);
        Debug.Log(pass.name);
        p2.SetActive(false);
        p3.SetActive(false);

        barReader = new BarcodeReader ();
		barReader.AutoRotate = true;
		barReader.TryInverted = true;

		if (!e_DeviceController) {
			e_DeviceController = GameObject.FindObjectOfType<DeviceCameraController>();
			if(!e_DeviceController)
			{
				Debug.LogError("the Device Controller is not exsit,Please Drag DeviceCamera from project to Hierarchy");
			}
		}
        //No iniciamos el QR, solo si el usuario desea realizar la lectura, asi ahorramos recursos.
        print("Device camera is working.");
        Debug.Log(e_DeviceController.name);
        StopWork();
	}
	
	void Update()
	{
        #region
#if UNITY_EDITOR
        if (framerate++ % 12== 0) {
#else
		if (framerate++ % 10== 0) {
#endif
            /*if (!e_DeviceController.isPlaying  ) {
				return;
			}*/

			if (e_DeviceController.isPlaying && !decoding && e_DeviceController.cameraTexture.isPlaying)
			{

				W = e_DeviceController.cameraTexture.width;					// get the image width
				H = e_DeviceController.cameraTexture.height;				// get the image height 

				if (W < 100 || H < 100) {
					return;
				}
				if(!isInit && W>100 && H>100)
				{

					blockWidth = (int)((Math.Min(W,H)/3f) *2);
		
					isInit = true;
				}

				if(targetColorARR == null)
				{
					targetColorARR= new Color32[blockWidth * blockWidth];
				}

				int posx = ((W-blockWidth)>>1);//
				int posy = ((H-blockWidth)>>1);
				
				orginalc = e_DeviceController.cameraTexture.GetPixels(posx,posy,blockWidth,blockWidth);// get the webcam image colors
				
                //convert the color(float) to color32 (byte)
				for(int i=0;i!= blockWidth;i++)
				{
					for(int j = 0;j!=blockWidth ;j++)
					{
						targetColorARR[i + j*blockWidth].r = (byte)( orginalc[i + j*blockWidth].r*255);
						targetColorARR[i + j*blockWidth].g = (byte)(orginalc[i + j*blockWidth].g*255);
						targetColorARR[i + j*blockWidth].b = (byte)(orginalc[i + j*blockWidth].b*255);
						targetColorARR[i + j*blockWidth].a = 1;
					}
				}

				// scan the qrcode 
				Loom.RunAsync(() =>
				              {
					try
					{
						Result data;
						data = barReader.Decode(targetColorARR,blockWidth,blockWidth);//start decode
						if (data != null) // if get the result success
						{
                            decoding = true;  // set the variable is true
                            dataText = data.Text;   // use the variable to save the code 
                            //Imrimimos lo leido y confirmamos que la lectura ha finalizado
                            print(dataText);
                            sc = true;
                        }

					}
					catch (Exception e)
					{
						decoding = false;
					}

				});	
			}
			//Si el QR se ha leido...
			if(sc)
			{
                input.text = dataText;
                p2.SetActive(true);
                p3.SetActive(false);
                StopWork();
            }
		}
	}
 	
	/// <summary>
	/// Reset this scan param
	/// </summary>
	public void Reset()
	{
		decoding = false;
		tempDecodeing = decoding;
	}
	
	/// <summary>
	/// Stops the work.
	/// </summary>
	public void StopWork()
	{
		decoding = true;
		if (e_DeviceController != null) {
			e_DeviceController.StopWork();
		}
	}
	
	/// <summary>
	/// Decodes the by static picture.
	/// </summary>
	/// <returns> return the decode result string </returns>
	/// <param name="tex">target texture.</param>
	public static string DecodeByStaticPic(Texture2D tex)
	{
		BarcodeReader codeReader = new BarcodeReader ();
		codeReader.AutoRotate = true;
		codeReader.TryInverted = true;
		
		Result data = codeReader.Decode (tex.GetPixels32 (), tex.width, tex.height);
		if (data != null) {
			return data.Text;
		} else {
			return "decode failed!";
		}
	}
    #endregion // Co
    // ------------------------------------------------------------ SEGUNDO PANEL ------------------------------------------------------------ 
    //Sin este metodo, una vez leido el QR podemos volver a entrar al lector, pero este ya no esta funcional
    public void activateqrpanel()
    {
        sc = false;
        decoding = false;
        e_DeviceController.StartWork();
        p3.SetActive(true);
        p2.SetActive(false);
    }
    public void desactivateqrpanel()
    {
        sc = true;
        decoding = true;
        e_DeviceController.StopWork();
        p3.SetActive(false);
        p2.SetActive(true);
    }

    public void seleccionerror()
    {
        seleccion.text = "prueba";
    }
    // ------------------------------------------------------------ PRIMER PANEL ------------------------------------------------------------ 
    String web= "http://angelmora.pythonanywhere.com/información/";
    public void infoweb()
    {
        Application.OpenURL(web);
    }
    
    public void onetotwo()
    {
        if(correo.text == "" && pass.text != "")
        {
            imageerror.SetActive(true);
            texterror.text = "Error al iniciar sesión: Debes introducir el correo electrónico.";
        }
        else if(pass.text == "" && correo.text != "")
        {
            imageerror.SetActive(true);
            texterror.text = "Error al iniciar sesión: Debes introducir la contraseña.";
        }
        else if (correo.text == "" && pass.text == "")
        {
            imageerror.SetActive(true);
            texterror.text = "Error al iniciar sesión:\nDebes introducir ambos campos.";
        }
        else
        {
            //Hacer aqui lo de la bbdd
            p1.SetActive(false);
            p2.SetActive(true);
            imageerror.SetActive(false);
        }
    }
}