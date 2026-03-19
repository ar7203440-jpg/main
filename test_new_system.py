# test_new_system.py - نئے ماڈیولز کی جانچ
import decision_engine
import analytics_bot
import learning_engine

print("="*50)
print("🔍 نیا سسٹم ٹیسٹ ہو رہا ہے")
print("="*50)

# 1. Analytics Bot ٹیسٹ
print("\n📊 Analytics Bot:")
analytics_bot.get_daily_report()

# 2. Decision Engine ٹیسٹ
print("\n🤔 Decision Engine:")
tasks = decision_engine.get_best_tasks()
print(tasks)

# 3. Learning Engine ٹیسٹ
print("\n🧠 Learning Engine:")
insights = learning_engine.analyze_performance()
print(insights)

print("\n✅ ٹیسٹ مکمل!")