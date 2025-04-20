using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class GameStateEvent:Event
    {
        public enum EventType { GameStart, GameEnd };
        EventType _type;
        public GameStateEvent(float timestamp, EventType type) : base(timestamp)
        {
            _type = type;
        }

        public override string getName() { return "GameStateEvent"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"Type\" : " + _type.ToString();
            s += "\n  }";
            return s;
        }




    }
}
