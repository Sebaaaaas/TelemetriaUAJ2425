using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle2EndEvent : Event
    {
        //private Guid gameID;
        public Puzzle2EndEvent(float timestamp/*, Guid _gameID*/) : base(timestamp)
        {
            //gameID = _gameID;
            name = "Puzzle2EndEvent";
        }
        public override string SerializeToJSON()
        {
            string s = "{";
            s += base.SerializeToJSON();
            //s += ", ";
            //s += "\"GameID\" : " + gameID;
            s += "}";
            return s;
        }
    }
}
