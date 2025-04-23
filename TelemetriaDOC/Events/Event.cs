using System;
using System.Collections.Generic;
using System.Data;
using System.Text;

using System;

namespace TelemetriaDOC
{
    public abstract class Event
    {
        protected string name;
        
        private Guid _id_session;
        private int _id_game;
        private long _timestamp;

        public Event()
        {
            name = "Event";
            _timestamp = new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();
        }

        public virtual string SerializeToJSON()
        {
            string s = "\"eventType\": \"" + name.ToString() + "\", ";
            s += "\"sessionID\":\"" + _id_session.ToString() + "\", ";
            s += "\"gameID\":\"" + _id_game.ToString() + "\", ";
            s += "\"timestamp\":" + _timestamp;
            return s;
        }
        public void SetSessionID(Guid sessionID) { _id_session = sessionID; }
        public void SetGameID(int gameID) { _id_game = gameID; }
    }
}
