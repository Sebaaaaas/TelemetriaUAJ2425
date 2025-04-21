using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle1StartEvent : Event
    {
       // private Guid gameID;
        public Puzzle1StartEvent(float timestamp/*, Guid _gameID*/) : base(timestamp)
        {
           // gameID = _gameID;
            name = "Puzzle1StartEvent";
        }
        public override string serializeToJSON()
        {
            string s = "{";
            s += base.serializeToJSON();
            //s += ", ";
            //s += "\"GameID\" : " + gameID;
            s += "}";
            return s;
        }
    }
}
