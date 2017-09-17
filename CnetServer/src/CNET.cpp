/*
 * CNET.cpp
 *
 *  Created on: 12.08.2016
 *      Author: pi
 */

#include "CNET.h"
#include "checksum.h"

/*
CNET::CNET() {
	// TODO Auto-generated constructor stub

}

CNET::~CNET() {
	// TODO Auto-generated destructor stub
}

*/

extern exlcm::cnet_crc_constants_t cnet_crc_constants_t;
extern exlcm::cnet_constants_t cnet_constants;


uint8_t CNET::Get_Command(char *command, uint8_t length, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
int maxcycles,cycles=0,num_data=0;

	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (num_data >= length) | (cycles > maxcycles) )
		{
//			cout << "Length: " << std::to_string(num_data) << " cycles: " << std::to_string(cycles) << endl;
			cout << "Length: "  << " cycles: "  << endl;
			command[length-1]= 0;
			cout << command << endl;
			return( false );
		}
		if( this->IsDataAvailable() )
		{
			command[num_data] = this->ReadByte(10);
//			cout << "<" << to_string(command[num_data]) << ">" << endl;
			if(command[num_data]!=0)
				num_data++;
		}
		else
		{
			sleep(SLEEP_TIME);
			cycles++;
		}
		if(num_data > 1)
		{
			if(  (command[num_data-2] == '<') & (command[num_data-1] == '\\')  )
			{
				command[num_data] = 0;
				return( true );
			}
		}

	}
	return( true );
}

uint8_t CNET::Get_Answer(char *answer, uint8_t length, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0,num_data=0;

	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (num_data >= length) | (cycles > maxcycles) )
		{
//			cout << "Length: " << to_string(num_data) << " cycles: " << to_string(cycles) << endl;
			answer[length-1]= 0;
			cout << answer << endl;
			return( false );
		}
		if( this->IsDataAvailable() )
		{
			cout << "Wait for answer" << endl;
			answer[num_data] = this->ReadByte(10000);		// war 10
//			cout << "<" << to_string(command[num_data]) << ">" << endl;
			if(answer[num_data]!=0)
				num_data++;
		}
		else
		{
			sleep(SLEEP_TIME);
			cycles++;
		}
		if(num_data > 1)
		{
			if(   ( (answer[num_data-2] == '.') | (answer[num_data-2] == '!') ) & (answer[num_data-1] == '>' )   )
			{
				answer[num_data] = 0;
				return( true );
			}
		}

	}
	return( true );
}

uint8_t CNET::Get_Command(string & command, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0;
unsigned int start,ende;
char one_char;

	command.clear();
	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (cycles > maxcycles) | (command.length()>1024) )
			return( false );
		if( this->IsDataAvailable() )
		{
			one_char = this->ReadByte(10);
			if( one_char != 0)
				command += one_char;
		}
		else
		{
			usleep(SLEEP_TIME);
			cycles++;
		}
		if(command.length() > 1)
		{
			ende = command.rfind("<\\",command.npos);
			start = command.rfind("\\>",command.npos);
			if(  ende < command.npos  )
			{
				if( start < command.npos )
				{
					command = command.substr(start+2,command.length()-4-start);
					return( true );
				}
				else
				{
					return( false );
				}
			}
		}

	}
	return( true );
}

uint8_t CNET::Get_Answer(string & answer,int16_t crc, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0;
char one_char;
size_t start;
	answer.clear();
	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
		{
      cout << "!!!!Timeout: "<<cycles << " von " << maxcycles << " erreicht" << endl;
			return( cnet_constants.timeout );
		}
	}
	while( 1 )
	{
		if( (cycles > maxcycles) | (answer.length()>1024) )
		{
    	cout << "---->!!!!Timeout: " <<cycles << " von " << maxcycles << " erreicht" << endl;
			return( cnet_constants.timeout );
		}
		if( this->IsDataAvailable() )
		{
			try
			{
//			  cout << "Read Character " << answer.length() << endl;
				one_char = this->ReadByte(timeout);
			}
			catch(...)
			{
				return( cnet_constants.timeout  );
			}
			if( one_char != 0)
				answer += one_char;
		}
		else
		{
//			cout << "Sleep for " << SLEEP_TIME << " us" << endl;
			usleep(SLEEP_TIME);
			cycles++;
		}
		if(answer.length() > 1)
		{

			if(crc==cnet_crc_constants_t.noCRC)
			{
				if(  (answer.rfind(".>",answer.npos) < answer.npos) | (answer.rfind("!>",answer.npos) < answer.npos)  )
				{
					start = answer.rfind("<",answer.npos);
					if( start < answer.npos )
					{
						answer = answer.substr(start+1,answer.length()-2-start);
						switch(*answer.rbegin())
						{
							case '.':
								return( cnet_constants.answerTrue ) ;
							break;
							case '!':
								return( cnet_constants.answerFalse ) ;
							break;
							default:
								return( cnet_constants.answerWrong ) ;
							break;
						}
					}
					else
					{
						return( cnet_constants.answerWrong );
					}
				}
			}
			else // with crc
			{
				size_t ende;
				string   answerCrc;
				ende = answer.rfind(">",answer.npos);
//				cout << "test 0" << endl;
				if( ende < answer.npos )
				{
					start = answer.rfind("<",answer.npos);
//					cout << "test 1 " << start << " " << ende << " " << answer.npos << endl;
					if( (start < answer.npos) && ( (answer[ende-5]=='.') || (answer[ende-5]=='!') ) )
					{
						answerCrc =  answer.substr(ende-4,4);
//						cout << "test 2" << endl;
						answer = answer.substr(start+1,answer.length()-6-start);
//						cout << "test 3" << endl;
						cout << "CRC: " << answerCrc << " Antwort: " << answer << endl;
						unsigned int crcInt,crc16;
						std::stringstream crcSS;
						crcSS << std::hex << answerCrc;
						crcSS >> crcInt;
						cout << "CRC: " << answerCrc << " = " << crcInt << " Antwort: " << answer << endl;
						crc16 = crc_xmodem( (const unsigned char*)  answer.c_str(),answer.length() );

						if(crc16==crcInt)
						{
							switch(*answer.rbegin())
							{
								case '.':
									return( cnet_constants.answerTrue ) ;
								break;
								case '!':
									return( cnet_constants.answerFalse ) ;
								break;
								default:
									return( cnet_constants.answerWrong ) ;
								break;
							}
						}
						else
						{
							cout << "CRC-Fehler" << endl;
							return(cnet_constants.crcError);
						}
					}
					else
					{
						cout << "answer wrong" << endl;
						return( cnet_constants.answerWrong );
					}
				}
			}
		}

	}
}


uint8_t CNET::Send_Command(string command,int16_t crc)
{
	if(this->IsOpen())
	{
		if(crc == cnet_crc_constants_t.noCRC)
			this->Write("\\>"+command+"<\\");
		else
		{
			uint16_t crc16;
			stringstream ss;
			crc16 = crc_xmodem((const unsigned char *)command.c_str(), command.length());
			ss << "\\>" << command << "<"  << std::setfill('0') << std::setw(4) << std::hex << crc16 << "\\" ;
			cout << ss.str() << endl;
			this->Write( ss.str() );
		}
		return(true);
	}
	else
		return(false);
}
