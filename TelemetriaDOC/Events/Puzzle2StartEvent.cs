using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle2StartEvent : Event
    {
        //private Guid gameID;
        public Puzzle2StartEvent(float timestamp/*, Guid _gameID*/) : base(timestamp)
        {
           // gameID = _gameID;
            name = "Puzzle2StartEvent";
        }
        public override string SerializeToJSON()
        {
            string s = "{";
            s += base.SerializeToJSON();
            //s += ", \"GameID\" : " + gameID;
            s += "}";
            return s;
        }
    }
}
