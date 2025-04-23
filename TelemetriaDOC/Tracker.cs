using System;
using System.Collections.Generic;
using System.Threading;

namespace TelemetriaDOC
{
    public class Tracker
    {
        private static Tracker instance = null;
        private Serializer serializer;
        private Persistence persistence;

        private Guid sessionID;
        private int gameID;
        private bool isFirstGame;

        private EventQueue eventQueue;
        // Temporizador para hacer flush a la cola de eventos
        private static Timer flushTimer;
        private Tracker()
        {
        }

        public static Tracker Instance()
        {
            return instance;
        }

        public static bool Init(Format format, Type type, string name, int sizeQueue, int timeBetweenFlush)
        {
            if (instance != null)
                return false;

            instance = new Tracker();
            
            // Para que los float se escriban siempre con "." en lugar de con ","
            System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("en-US");

            //Iniciar serializador
            instance.InitSerializer(format);

            //Iniciar persistencia
            if(!instance.InitPersistence(type, name))
                return false;

            instance.eventQueue = new EventQueue(sizeQueue);

            instance.sessionID = Guid.NewGuid();
            instance.gameID = 0;
            instance.isFirstGame = true;

            flushTimer = new Timer(_ => instance.Flush(), null, 0, timeBetweenFlush);

            return true;
        }

        public void InitSerializer(Format format)
        {
            switch (format)
            {
                case Format.JSON:
                    instance.serializer = new SerializerJSON();
                    break;
            }
        }

        public bool InitPersistence(Type typeSave, string name)
        {
            switch (typeSave)
            {
                case Type.Disk:
                    instance.persistence = new DiskPersistence();
                    return ((DiskPersistence)instance.persistence).Init(name, instance.serializer);

                default:
                    return false;
            }
        }

        public static void TrackEvent(Event e) 
        {
            if (instance == null)
                return;

            e.SetSessionID(instance.sessionID);

            // Si el evento corresponde a un inicio de partida se incrementa el contador gameID
            if (e is GameStateEvent gameStateEvent && gameStateEvent.GetEventType() == GameStateEvent.EventType.GameStart) 
            {
                // En la primera partida no se incrementa el contador para que el gameID sea el mismo
                // que el del evento de inicio de sesion
                if (!instance.isFirstGame) instance.gameID++;
                else instance.isFirstGame = false;
            }

            e.SetGameID(instance.gameID);
            instance.eventQueue.AddEvent(e);
        }

        public void Flush()
        {
            string text = "";
            
            // Serializamos cada evento de la cola
            while(eventQueue.queue.Count > 0)
            {
                text += instance.serializer.Serialize(eventQueue.queue.Dequeue());
            }

            eventQueue.queue.Clear();

            instance.persistence.Write(text);            
        }

        public static void Closing()
        {
            if (instance == null)
                return;

            instance.CloseFile();
        }
        private void CloseFile()
        {

            flushTimer.Dispose();
            instance.Flush();
            instance.persistence.Write(instance.serializer.SerializerEnding());
            instance.persistence.Close();
        }
    }
}