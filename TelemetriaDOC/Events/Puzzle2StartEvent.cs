using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle2StartEvent : Event
    {
        private Guid gameID;
        public Puzzle2StartEvent(float timestamp, Guid _gameID) : base(timestamp)
        {
            gameID = _gameID;
            name = "Puzzle2StartEvent";
        }
        public override string serializeToJSON()
        {
            string s = "{";
            s += base.serializeToJSON();
            s += ", \"GameID\" : " + gameID;
            s += "}";
            return s;
        }
    }
}
