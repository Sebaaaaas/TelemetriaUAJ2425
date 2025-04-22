using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Format { JSON };
    interface Serializer
    {
        string Serialize(Event e);
        string GetExtension();

        string SerializerEnding();
    }
}
