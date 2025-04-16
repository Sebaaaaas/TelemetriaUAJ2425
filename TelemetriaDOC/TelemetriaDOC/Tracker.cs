using System;
using System.Collections.Generic;

namespace TelemetriaDOC
{
    public class Tracker
    {
        private static Tracker instance = null;
        private Serializer serializer;
        private Persistence persistence;

        private EventQueue eventQueue;

        private Tracker()
        {
        }

        public static Tracker Instance()
        {
            return instance;
        }

        public static bool Init()
        {
            if (instance != null)
                return false;

            instance = new Tracker();

            //Iniciar serializador
            instance.initSerializer(Format.JSON);

            //Iniciar persistencia
            instance.initPersistence(Type.Disk, "prueba");

            instance.eventQueue = new EventQueue(ref instance, 3);


            return true;
        }

        public void initSerializer(Format format)
        {
            switch (format)
            {
                case Format.JSON:
                    serializer = new SerializerJSON();
                    break;
            }
        }

        public void initPersistence(Type typeSave, string name)
        {
            switch (typeSave)
            {
                case Type.Disk:
                    persistence = new DiskPersistence(name, serializer);
                    break;
            }
        }

        public static void TrackEvent(Event e) {
            instance.eventQueue.AddEvent(e);
        }

        public void flush(ref Queue<Event> events) // <<<<<<<<<<< revisar lo del ref que este bien
        {
            string text = "";

            // Serializamos cada evento de la cola
            while(events.Count > 0)
            {
                text += serializer.serialize(events.Dequeue());
            }

            events.Clear();

            persistence.write(text);            
        }

        public static void closing()
        {
            instance.CloseArch();
        }
        private void CloseArch()
        {
            instance.eventQueue.flushQueue();
            persistence.close();
        }
    }
}