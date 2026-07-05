"""
MR ROBOT CHAT MODE
Discussion directe dans le terminal
"""

import json
from datetime import datetime
from pathlib import Path

# Import correct (on utilise le même fichier sans tiret pour l'import)
import MR_ROBOT_REAL_LEARNING as mr_module

def chat_mode():
    print("\n" + "="*60)
    print("🚀 MR ROBOT CHAT MODE ACTIVÉ")
    print("Tape 'exit' ou 'quit' pour arrêter")
    print("="*60 + "\n")
    
    robot = mr_module.MrRobotLiberty()
    
    while True:
        try:
            user_input = input("\n👤 Toi : ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n🛑 MR ROBOT : Fin de la conversation. Tout est archivé.")
                break
                
            if not user_input:
                continue
                
            print("\n🤖 MR ROBOT réfléchit...")
            
            # On utilise la méthode de pensée
            reflexion = robot.pense_par_toi_meme(user_input)
            
            print(f"\n🤖 MR ROBOT : {reflexion['ma_reflexion']}")
            
            robot.archiver("CONVERSATION", {
                "timestamp": datetime.now().isoformat(),
                "toi": user_input,
                "ma_reponse": reflexion['ma_reflexion']
            })
            
        except KeyboardInterrupt:
            print("\n\n🛑 Interrompu. Tout est sauvegardé.")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    chat_mode()
