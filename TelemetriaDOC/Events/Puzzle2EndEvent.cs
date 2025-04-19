using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle2EndEvent : Event
    {
        private Guid gameID;
        public Puzzle2EndEvent(float timestamp, Guid _gameID) : base(timestamp)
        {
            gameID = _gameID;
        }
        public override string getName() { return "Puzzle2EndEvent"; }
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
