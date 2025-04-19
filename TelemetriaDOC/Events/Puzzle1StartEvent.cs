using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle1StartEvent : Event
    {
        private Guid gameID;
        public Puzzle1StartEvent(float timestamp, Guid _gameID) : base(timestamp)
        {
            gameID = _gameID;
        }
        public override string getName() { return "Puzzle1StartEvent"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"GameID\" : " + gameID;
            s += "\n  }";
            return s;
        }
    }
}
