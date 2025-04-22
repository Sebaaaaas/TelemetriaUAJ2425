using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class GameStateEvent:Event
    {
        public enum EventType { GameStart, GameEnd };
        public enum ResultType { Sucess, Fail,Quit };
        EventType _type;
        ResultType _res;
        public GameStateEvent(float timestamp, EventType type, ResultType result) : base(timestamp)
        {
            name = type.ToString();
            _type = type;
            _res = result; //0 = Success / 1 = Fail / 2 = Quit
        }

        public override string SerializeToJSON()
        {
            string s = "{";
            s += base.SerializeToJSON();
            if(_type == EventType.GameEnd ) {
                if (_res==ResultType.Sucess)
                {
                    s += ", \"RESULT\": \"SUCCESS\"";
                }
                else if (_res== ResultType.Fail) 
                {
                    s += ", \"RESULT\": \"FAIL\"";
                }
                else
                {
                    s += ", \"RESULT\": \"QUIT\"";  //Si existe QUIT y no hay ningun SUCCESS entonces implica que el jugador abandona
                }
            
            }
            s += "}";
            return s;
        }




    }
}
