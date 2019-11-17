using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;

namespace chatClient
{
    public partial class Form1 : Form
    {
        Socket sck;
        IPEndPoint serverEP;
        IPEndPoint clientEP;
        EndPoint remote;
        bool connected = false;

        public Form1()
        {
            InitializeComponent();
        }

        private void btConnect_Click(object sender, EventArgs e)
        {
            createConnection();
        }

        private void btDisconnect_Click(object sender, EventArgs e)
        {
            disconnect();
        }

        private void btSend_Click(object sender, EventArgs e)
        {
            sendMessage();
        }

        private void createConnection()
        {
            // create socket
            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            // bind socket
            string clientIP = tbClientIP.Text;
            int clientPort = int.Parse(tbClientPort.Text);
            clientEP = new IPEndPoint(IPAddress.Parse(clientIP), clientPort);
            sck.Bind(clientEP);

            // make connection to the server
            string serverIP = tbServerIP.Text;
            int serverPort = int.Parse(tbServerPort.Text);
            serverEP = new IPEndPoint(IPAddress.Parse(serverIP), serverPort);
            sck.Connect(serverEP);
            remote = (EndPoint)(serverEP);

            // enable send button and state
            btSend.Enabled = true;
            connected = true;
            
            // start a listening thread
            Thread thread = new Thread(serverHandler);
            thread.IsBackground = true;
            thread.Start();
        }

        private void serverHandler()
        {
            string message;
            while (connected)
            {
                try
                {
                    byte[] buffer = new byte[1024];
                    int recv = sck.ReceiveFrom(buffer, ref remote);
                    message = Encoding.ASCII.GetString(buffer, 0, recv);
                    libChat.Items.Add(message);
                }
                catch (SocketException) { }
            }
        }

        private void disconnect()
        {
            connected = false;
            sck.Close();
            btSend.Enabled = false;
        }

        private void sendMessage()
        {

        }
    }
}
