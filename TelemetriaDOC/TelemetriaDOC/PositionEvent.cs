using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class PositionEvent : Event
    {
        private int _x;
        private int _y;
        private int _z;
        public PositionEvent(int id_session, float timestamp, int posx, int posy, int posz) : base(id_session, timestamp)
        {
            _x = posx;
            _y = posy;
            _z = posz;
        }
        public override string getName() { return "TestEvent"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"Position X\" : " + _x + ",\n" + "    \"Position Y\" : " + _y + ",\n" + "    \"Position Z\" : " + _z;
            s += "\n  }\n";
            return s;
        }
    }
}