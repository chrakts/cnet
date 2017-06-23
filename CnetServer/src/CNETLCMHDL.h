/*
 * CNETLCMHDL.h
 *
 *  Created on: 13.08.2016
 *      Author: pi
 */

#ifndef CNETLCMHDL_H_
#define CNETLCMHDL_H_

#include <stdio.h>

#include <lcm/lcm-cpp.hpp>			// include der library
#include "lcm-cnet/exlcm/lcm_cnet.hpp"
#include "CNET.h"
#include <cstdint>
#include <iostream>

using namespace std;

extern CNET cnet;
extern lcm::LCM cnet_lcm;

extern exlcm::cnet_command_t cnet_command;

class CNET_LCM_HDL
{
public:
//	CNET_LCM_HDL();
	virtual ~CNET_LCM_HDL();

	void handle_cnet_command(const lcm::ReceiveBuffer *rbuf, const std::string &chan, const exlcm::cnet_command_t* msg)
	{
		cout << "Folgendes Kommando erhalten: " << msg->command << endl;
		cnet_command = *msg;
	}
};

#endif /* CNETLCMHDL_H_ */
