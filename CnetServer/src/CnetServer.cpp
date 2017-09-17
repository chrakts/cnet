//============================================================================
// Name        : CnetServer.cpp
// Author      : C. Abel/Keilhack
// Version     :
// Copyright   : All for free
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <SerialStream.h>
#include <SerialPort.h>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <thread>
#include <chrono>
#include <inttypes.h>
#include <lcm/lcm-cpp.hpp>			// include der library
#include "lcm-cnet/exlcm/lcm_cnet.hpp"			// Sammelinclude fuer alle lcm-includes
#include "CNET.h"
#include "CNETLCMHDL.h"
#include "checksum.h"
#include "argparse.h"

using namespace std;
using namespace LibSerial;


SerialPort::BaudRate convertBaudrate(uint32_t baudInt);


SerialPort::BaudRate convertBaudrate(uint32_t baudInt)
{
uint32_t BaudRatesInt[] = {50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200,230400,460000,5000000,576000,921600,1000000,0};

SerialPort::BaudRate BaudRatesSerial[] = {SerialPort::BAUD_50,SerialPort::BAUD_75,SerialPort::BAUD_110,SerialPort::BAUD_134,SerialPort::BAUD_150,SerialPort::BAUD_200,
		SerialPort::BAUD_300,SerialPort::BAUD_600,SerialPort::BAUD_1200,SerialPort::BAUD_1800,SerialPort::BAUD_2400,SerialPort::BAUD_4800,SerialPort::BAUD_9600,
		SerialPort::BAUD_19200,SerialPort::BAUD_38400,SerialPort::BAUD_57600,SerialPort::BAUD_115200,SerialPort::BAUD_230400,SerialPort::BAUD_460800,SerialPort::BAUD_500000,
		SerialPort::BAUD_576000,SerialPort::BAUD_921600,SerialPort::BAUD_1000000};
int i = 0;
	while( BaudRatesInt[i]!=baudInt && (BaudRatesInt[i]!=0) )
		i++;
	if(BaudRatesInt[i]!=0)
		return(BaudRatesSerial[i]);
	else
	{
		i=0;
		while( BaudRatesSerial[i]!=SerialPort::BAUD_DEFAULT && (BaudRatesInt[i]!=0) )
			i++;
		cout << "Unbekannte Baudrate, setze die Baudrate auf default-Baudrate: " << BaudRatesInt[i] << endl;
		return(SerialPort::BAUD_DEFAULT);
	}
}

lcm::LCM cnet_lcm("udpm://239.255.76.67:7667?ttl=1");
exlcm::cnet_command_t cnet_command;
exlcm::cnet_constants_t cnet_constants;
exlcm::cnet_crc_constants_t cnet_crc_constants_t;


static const char *const usages[] =
{
    "test_argparse [options] [[--] args]",
    "test_argparse [options]",
    NULL,
};

int main(int argc, const char **argv)
{
exlcm::cnet_answer_t lcm_answer;
string answer;


// ------------------- Kommandozeilenauswertung --------------------------------------


	const char *device = NULL;
	const char *channel = "CNET";
	int baudRate=57600;

	struct argparse_option options[] = {
		OPT_HELP(),
		OPT_GROUP("Schnittstelle"),
		OPT_STRING('d', "device", &device, "device for CNET-connection (e.g. /dev/ttyUSB0)"),
		OPT_INTEGER('b', "baud", &baudRate, "Baudrate (default: 57600)"),
		OPT_GROUP("CNET-Optionen"),
		OPT_STRING('c', "channel", &channel, "Channel for CNET-connection (lcm-Kanal)"),

	//	OPT_BOOLEAN('f', "force", &force, "force to do"),
	//    OPT_BIT(0, "read", &perms, "read perm", NULL, PERM_READ, OPT_NONEG),
		OPT_END(),
	};

	struct argparse argparse;
	argparse_init(&argparse, options, usages, 0);
	argparse_describe(&argparse, "\nStellt einen Server für das CNET zur Verfügung, der über LCM erreichbar ist.", "\nAdditional description of the program after the description of the arguments.");
	argc = argparse_parse(&argparse, argc, argv);
	printf("path: %s\n", device);
	printf("Baudrate: %d\n", convertBaudrate(baudRate));
	printf("Kanal: %s\n", channel);
	if (argc != 0)
	{
		printf("argc: %d\n", argc);
		int i;
		for (i = 0; i < argc; i++)
		{
			printf("argv[%d]: %s\n", i, *(argv + i));
		}
	}
// ------------------- Ende Kommandozeilenauswertung --------------------------------------

	CNET cnet(device);
	cout << endl << "----- Here is the CNET-Server -----" << endl << endl; // prints Here is the CNET/Server

	cnet.Open(convertBaudrate(baudRate),SerialPort::CHAR_SIZE_8,SerialPort::PARITY_NONE,SerialPort::STOP_BITS_1,SerialPort::FLOW_CONTROL_NONE);

	if( cnet.IsOpen()==false )
		cout << "Fehler beim Öffnen des Serial-Port" << endl;
	else
	{
		cnet.Close();
		cout << "Serial-Port erfolgreich geöffnet." << endl;
		if( !cnet_lcm.good())
			cout << "LCM-Init fehlgeschlagen" << endl;
		else
		{
			cout << "LCM-Init erfolgreich" << endl;
			CNET_LCM_HDL cnet_lcm_hdl;
			cnet_lcm.subscribe(channel,&CNET_LCM_HDL::handle_cnet_command,&cnet_lcm_hdl);

			cout << "Waiting for command" << endl;
		}
//		while( cnet_lcm.handle() == 0);
		while(1)
		{
			while( cnet_lcm.getFileno() == -1);
				cnet_lcm.handle();

			if(cnet_command.command.compare(0,9,"ServerIO?")==0) // dient zur internen Serverabfrage
			{
				lcm_answer.answer = "iO.";
				lcm_answer.error = cnet_constants.answerTrue;
				cnet_lcm.publish(cnet_command.target,&lcm_answer);
				cout << "Answer publiziert" << endl;
			}
			else
			{
				cnet.Open(convertBaudrate(baudRate),SerialPort::CHAR_SIZE_8,SerialPort::PARITY_NONE,SerialPort::STOP_BITS_1,SerialPort::FLOW_CONTROL_NONE);
				cnet.Send_Command(cnet_command.command,cnet_command.crcType);
				cout << "Command #" << cnet_command.command << "# gesendet über RS485" << endl;
				if(cnet_command.expect_answer)
				{
					cout << "Wait for Answer for " <<  (uint16_t)cnet_command.timeout_ms << " ms" << endl;
					lcm_answer.error = cnet.Get_Answer(answer,cnet_command.crcType,(uint16_t)cnet_command.timeout_ms);
					switch( lcm_answer.error ) //cnet.Get_Answer(answer,5)
					{
						case cnet_constants.answerTrue:
						case cnet_constants.answerFalse:
							lcm_answer.answer = answer;
						break;
						case cnet_constants.answerWrong:
							lcm_answer.answer = "Server-Wrong-Answer!";
						break;
						case cnet_constants.timeout:
							lcm_answer.answer = "Server-Timeout!";
						break;
						case cnet_constants.crcError:
							lcm_answer.answer = "Server-CRC-Error!";
						break;

					}
					cout.flush();
					cnet_lcm.publish(cnet_command.target,&lcm_answer);
					cout << "Answer " << lcm_answer.answer << " publiziert, Status: "  << endl;
					cout << "Answer ::" << lcm_answer.answer << ":: an !" << cnet_command.target << "!  publiziert, Status: "  << endl;
				}
				cnet.Close();

			}

		}
	}
	return 0;
}

