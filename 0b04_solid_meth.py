from abc import ABC, abstractmethod
import random # для смены оружия

# Создаем класс, описывающий результат атаки
class AttackResult:
    def __init__(self, success: bool, damage: int, description: str):
        self.success = success
        self.damage = damage
        self.description = description

    # Добавляем вывод результатов борьбы
    def __str__(self):
        return f"{self.description} (Урон: {self.damage}, Успех: {self.success})"

# Создаем абстрактный класс защиты для чудовища
class Defense(ABC):
    @abstractmethod
    def absorb_damage(self, damage: int) -> int:
        pass

# Создаем подклассы защиты чудовища: их три - без защиты - возвращает урон после применения защиты, броня и волшебный щит,
# логика: победа завит не от типа оружия, а от success; int показывает степень урона при применении разного оружия
# и выражается целым числом.
class NoDefense(Defense):
    def absorb_damage(self, damage: int) -> int:
      return damage

class Armor(Defense):
    def absorb_damage(self, damage: int) -> int:
        reduced = max(damage - 10,0)
        return reduced

class MagicShield(Defense):
    def absorb_damage(self, damage: int) -> int:
        return damage // 2  # поглощает половину урона

# Создаем абстрактный класс - оружие
class Weapon(ABC):
    @abstractmethod
    def attack(self) -> AttackResult:
        pass

# Создаем подклассы оружия: их три - меч, лук и кинжал, логика: победа завит не от типа оружия, а от success;
# int показывает степень урона при применении разного оружия, выражается целым числом
class Sword(Weapon):
    def attack(self) -> AttackResult:
        return AttackResult(True, 30, "Боец рубит мечом")

class Bow(Weapon):
    def attack(self) -> AttackResult:
        return AttackResult(True, 20, "Боец стреляет из лука")

class Dagger(Weapon):
    def attack(self) -> AttackResult:
        return AttackResult(True, 10, "Боец колет кинжалом")

# Создаем класс чудовища и определяем ему устойчивость от атак (здоровье)
class Monster:
    def __init__(self, name: str, health: int = 100, defense: Defense = None):
        self.name = name
        self.health = health  # Текущее здоровье (меняется при атаке)
        self.max_health = health  # Максимальное здоровье (не меняется)
        self.defense = defense or NoDefense()

    # Методы определяют пораженность и гибель чудовища
    def take_damage(self, damage: int):
        actual_damage = self.defense.absorb_damage(damage)
        self.health -= actual_damage

    def is_defeated(self) -> bool:
            return self.health <= 0

# Создаем класс бойца - он атакует
class Fighter:
    def __init__(self, name: str, weapon: Weapon):
        self.name = name
        self.weapon = weapon

    # Меняем вид оружия
    def change_weapon(self, new_weapon: Weapon):
        self.weapon = new_weapon

    # Метод возвращает исход атаки (AttackResult)
    def perform_attack(self) -> AttackResult:
        return self.weapon.attack()

# Создаем класс смены оружия: оружие меняется случайным методом
class WeaponSelector:
    def __init__(self, available_weapons: list[Weapon]):
        self.available_weapons = available_weapons

    def get_random_weapon(self) -> Weapon:
        return random.choice(self.available_weapons)

# Создаем класс боя - отдельная сущность, не зависит от бойца и чудовища
class Duel:
    def __init__(self, fighter: Fighter, monster: Monster):
        self.fighter = fighter
        self.monster = monster

    # Метод выводит описание атаки self.fighter.perform_attack() вызывает метод attack() у текущего оружия бойца attack() возвращает объект AttackResult,
    # который содержит текстовое описание действия, нанесённый урон и результат.
    def start(self):
      for round_number in range(1, 4): # три раунда боя
        print(f"\nРаунд {round_number}:")
        result = self.fighter.perform_attack()
        print(result.description)

        if result.success:
            self.monster.take_damage(result.damage)
            print(f"{self.monster.name} получает урон {result.damage}")
            print(f"Осталось здоровья: {self.monster.health} HP") # HP - количество здоровья (Health Points)

            if self.monster.is_defeated():
                print(f"{self.monster.name} побеждён!")
                print("Игра завершена.")
                return
            else:
                print(f"Атака не удалась.{self.monster.name} не пострадал.")

      print("\nРаунды закончились.")
      if self.monster.is_defeated():
          print(f"{self.monster.name} побеждён!")
      else:
          print(f"{self.monster.name} выжил с {self.monster.health} HP.")
      print("Игра завершена.")

if __name__ == "__main__":
    # Создаём оружие
    sword = Sword()
    bow = Bow()
    dagger = Dagger()

    # Создаём бойца с начальным оружием
    fighter = Fighter(name="Герой", weapon=sword)

    # Создаём монстра с бронёй
    monster = Monster(name="Дракон", health=100, defense=Armor())

    # Запускаем бой
    duel = Duel(fighter, monster)
    duel.start()

    # Случайная смена оружия
    selector = WeaponSelector([sword, bow, dagger])
    fighter.change_weapon(selector.get_random_weapon())

    # Новый бой
    duel = Duel(fighter, monster)
    duel.start()











