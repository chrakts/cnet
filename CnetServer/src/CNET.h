/*
 * CNET.h
 *
 *  Created on: 12.08.2016
 *      Author: pi
 */

#ifndef CNET_H_
#define CNET_H_

#include <iostream>   // std::cout
#include <SerialStream.h>
#include <SerialPort.h>
#include <string>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <sstream>

#include <lcm/lcm-cpp.hpp>			// include der library
#include "lcm-cnet/exlcm/lcm_cnet.hpp"			// Sammelinclude fuer alle lcm-includes
#include "checksum.h"

using namespace std;
using namespace LibSerial;

class CNET: public SerialPort
{
	public:
		using SerialPort::SerialPort;

		~CNET()
		{
			this->Close();
		}
		uint8_t Get_Command(char *command, uint8_t length, uint16_t timeout);
		uint8_t Get_Answer(char *answer, uint8_t length, uint16_t timeout);
		uint8_t Get_Command(string & command, uint16_t timeout);
		uint8_t Get_Answer(string & answer,int16_t crc, uint16_t timeout);
		uint8_t Send_Command(string command,int16_t crc);

};

#endif /* CNET_H_ */
