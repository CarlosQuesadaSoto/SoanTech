using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class QRDecodeTest : MonoBehaviour
{
	public QRCodeDecodeController e_qrController;

	public Text UiText;

	public GameObject resetBtn;

	public GameObject scanLineObj;

	private void Start()
	{
		if (this.e_qrController != null)
		{
			this.e_qrController.onQRScanFinished += new QRCodeDecodeController.QRScanFinished(this.qrScanFinished);
		}
	}

	private void Update()
	{
	}

	private void qrScanFinished(string dataText)
	{
        this.UiText.text = dataText;
        //SceneManager.LoadScene("Incidencia");
        if (this.resetBtn != null)
		{
			this.resetBtn.SetActive(true);
		}
		if (this.scanLineObj != null)
		{
			this.scanLineObj.SetActive(false);
		}
        
    }

	public void Reset()
	{
		if (this.e_qrController != null)
		{
			this.e_qrController.Reset();
		}
		if (this.UiText != null)
		{
			this.UiText.text = string.Empty;
		}
		if (this.resetBtn != null)
		{
			this.resetBtn.SetActive(false);
		}
		if (this.scanLineObj != null)
		{
			this.scanLineObj.SetActive(true);
		}
	}

	public void GotoNextScene()
	{
        if (this.e_qrController != null)
        {
            this.e_qrController.StopWork();
        }
        /*Application.DontDestroyOnLoad(gameObject);*/
		Application.LoadLevel("Incidencia");
	}
}
