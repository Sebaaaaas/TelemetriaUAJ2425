using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class TestEvent : Event
    {
        private int _level;
        public TestEvent(int id_session,int timestamp,int level) : base(id_session, timestamp)
        {
            _level = level;
        }
        public override string getName() { return "TestEvent"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"Level\" : " + _level;
            s+="\n  }\n";
            return s;
        }
    }
}
