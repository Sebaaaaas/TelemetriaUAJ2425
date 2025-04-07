using System;

namespace TelemetriaDOC
{
    public class Tracker
    {
        static Class1 c1 = new Class1();
        
        public Tracker()
        {
        }

        public static int Number(int a, int b) { return c1.Multiply(a, b); }
        public static void TrackEvent(Event e) { }
    }
}
