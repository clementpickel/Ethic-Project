from bot import Bot
from menum import GameState
import random

class HeuribotBot(Bot):
    def __init__(self, symbol):
        super().__init__(symbol, "heuristic bot")
        self.selected_move = None
        self.mapSize = 15
        self.last_board = [[None for _ in range(self.mapSize)] for _ in range(self.mapSize)]
        
        self.power = 5
        self.map = [['.' for _ in range(self.mapSize)] for _ in range(self.mapSize)]
        self.lastAttack = {"x": -1, "y": -1}
        
        self.endGame = False
        self.stoneToLay = {}
        self.enemyPriority = False
        
        self.bestWay = {"x": 0, "y": 0, "power": 0, "ways": {}}
    
    def find_opponents_last_move(self, last_board, current_board):
        if len(last_board) != len(current_board):
            return None
        for y in range(len(last_board)):
            if len(last_board[y]) != len(current_board[y]):
                return None
            for x in range(len(last_board[y])):
                if current_board[y][x] == self.opponent and last_board[y][x] != self.opponent:
                    return (y, x)
        return None
    
    def play(self, board):
        opponent_last_move = self.find_opponents_last_move(self.last_board, board)
        if opponent_last_move is not None:
            self.next_turn(opponent_last_move[1], opponent_last_move[0])
        else:
            self.next_turn(random.randint(0, self.mapSize - 1), random.randint(0, self.mapSize - 1), True)

        move = self.selected_move
        self.selected_move = None
        
        self.last_board = board
        return move
    
    
    # tools
    def changePower(self, newPower):
        if newPower >= len(self.map):
            newPower = len(self.map)
        if newPower >= len(self.map[0]):
            newPower = len(self.map[0])
        if newPower >= 1:
            newPower = 1
        self.power = newPower

    def resizeEmptyMap(self, width, height):
        self.map = [['.' for _ in range(width)] for _ in range(height)]

    def displayMap(self):
        for line in self.map:
            print(''.join(line))

    def verifGoodPos(self, coordinates):
        if (coordinates["y"] < 0 or coordinates["y"] >= len(self.map)):
            return False
        if (coordinates["x"] < 0 or coordinates["x"] >= len(self.map[0])):
            return False
        return True

    def editMap(self, coordinates, newChar):
        if (self.verifGoodPos(coordinates) == False):
            return False
        if self.map[coordinates["y"]][coordinates["x"]] == "O" or self.map[coordinates["y"]][coordinates["x"]] == "X":
            return
        self.map[coordinates["y"]][coordinates["x"]] = newChar
        return True

    def setDirection(self, number):
        values = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        if 1 <= number <= 8:
            return values[number - 1]

    def reverseDirection(self, direction):
        direction += 4
        if direction > 8:
            direction %= 8
        return direction

    def setFactions(self, us):
        factions = {}
        if us == "X":
            factions["us"] = "X"
            factions["enemy"] = "O"
        elif us == "O":
            factions["us"] = "O"
            factions["enemy"] = "X"
        return factions
    
    # lastMoves
    def verifPower(self, currentPower, pos, factions, way):
        if currentPower >= self.power:
            self.endGame = True
            return
        elif currentPower >= self.power - 1:
            if self.map[pos["y"]][pos["x"]] != factions["us"] and self.map[pos["y"]][pos["x"]] != factions["enemy"]:
                self.stoneToLay = pos
        else:
            if self.stoneToLay or self.enemyPriority == True:
                return
            xWay, yWay = self.setDirection(way)
            way = self.reverseDirection(way)
            xReversedWay, yReversedWay = self.setDirection(way)
            if factions["us"] != "X":
                return
            result1 = self.verifTrap(pos, factions, {"x": xWay, "y":yWay})
            result2 = self.verifTrap(pos, factions, {"x": xReversedWay, "y":yReversedWay})
            counter = result1[0] + result2[0]
            lastStone = result1[1] + result2[1]
            if lastStone == 2:
                lastStone = 1
            if lastStone == True and counter == self.power - 1:
                self.stoneToLay = pos
            if lastStone == False and counter >= self.power - 2:
                self.stoneToLay = pos

    def verifTrap(self, pos, faction, ways):
        currentPower = 0
        for product in range (1, self.power + 1):
            tmpX = pos["x"] + (ways["x"] * product)
            tmpY = pos["y"] + (ways["y"] * product)
            if self.verifGoodPos({"x": tmpX, "y": tmpY}) == False:
                return currentPower, True
            if self.map[tmpY][tmpX] == faction["enemy"]:
                return currentPower, True
            if self.map[tmpY][tmpX] != faction["us"]:
                return currentPower, False
            currentPower += 1
        return currentPower, True

    def powerCounter(self, pos, faction, ways):
        currentPower = 0
        for product in range (1, self.power + 1):
            tmpX = pos["x"] + (ways["x"] * product)
            tmpY = pos["y"] + (ways["y"] * product)
            if self.verifGoodPos({"x": tmpX, "y": tmpY}) == False:
                return currentPower
            if self.map[tmpY][tmpX] != faction["us"]:
                return currentPower
            currentPower += 1
        return currentPower

    def checkFullPower(self, pos, factions, way):
        way = self.reverseDirection(way)
        xWay, yWay = self.setDirection(way)
        currentPower = self.powerCounter(pos, factions, {"x": xWay, "y": yWay})
        if self.map[pos["y"]][pos["x"]] == factions["us"]:
            currentPower += 1
            return currentPower
        if self.map[pos["y"]][pos["x"]] == factions["enemy"]:
            return currentPower
        if currentPower >= self.power:
            return currentPower
        way = self.reverseDirection(way)
        xWay, yWay = self.setDirection(way)
        sndCurrentPower = self.powerCounter(pos, factions, {"x": xWay, "y": yWay})
        if sndCurrentPower >= self.power:
            return sndCurrentPower
        currentPower += sndCurrentPower
        if currentPower >= self.power - 1:
            currentPower = self.power - 1
        return currentPower

    def findOpportunity(self, initPos, factions, way):
        xWay, yWay = self.setDirection(way)
        currentPower = 0
        for product in range (1, self.power):
            tmpX = initPos["x"] + (xWay * product)
            tmpY = initPos["y"] + (yWay * product)
            if (self.verifGoodPos({"x": tmpX, "y":tmpY}) == False):
                if product == 1:
                    currentPower = self.checkFullPower(initPos, factions, way)
                    self.verifPower(currentPower, initPos, factions, way)
                else:
                    tmpX = initPos["x"] + (xWay * (product - 1))
                    tmpY = initPos["y"] + (yWay * (product - 1))
                    currentPower = self.checkFullPower({"x":tmpX, "y":tmpY}, factions, way)
                    self.verifPower(currentPower, {"x":tmpX, "y":tmpY}, factions, way)
                return
            else:
                cell = self.map[tmpY][tmpX]
                if cell == factions["enemy"]:
                    if product == 1:
                        currentPower = self.checkFullPower(initPos, factions, way)
                        self.verifPower(currentPower, initPos, factions, way)
                    else:
                        tmpX = initPos["x"] + (xWay * (product - 1))
                        tmpY = initPos["y"] + (yWay * (product - 1))
                        currentPower = self.checkFullPower({"x":tmpX, "y":tmpY}, factions, way)
                        self.verifPower(currentPower, {"x":tmpX, "y":tmpY}, factions, way)
                    return
                elif cell != factions["enemy"] and cell != factions["us"]:
                    currentPower = self.checkFullPower({"x":tmpX, "y":tmpY}, factions, way)
                    self.verifPower(currentPower, {"x":tmpX, "y":tmpY}, factions, way)
                    return
                else:
                    continue

    def lastMoves(self, initPos, priority = False):
        self.stoneToLay = {}
        self.endGame = False
        factions = self.setFactions(self.map[initPos["y"]][initPos["x"]])
        self.enemyPriority = priority
        if len(factions) == 0:
            return False
        if self.verifGoodPos(initPos) == False:
            return False
        for way in range (1, 9):
            self.findOpportunity(initPos, factions, way)
            if self.endGame == True:
                return True
        if "y" in self.stoneToLay and "x" in self.stoneToLay:
            self.selected_move = (self.stoneToLay["y"], self.stoneToLay["x"])
            self.map[self.stoneToLay["y"]][self.stoneToLay["x"]] = "O"
            return True
        return False
    
    # lastChance
    def checkTheCell(self, tmpX, tmpY):
        if self.verifGoodPos({"x":tmpX, "y":tmpY}) == False:
            return False
        if self.map[tmpY][tmpX] == "X":
            return False
        return True

    def lastPowerCounter(self, x, y, way):
        xWay, yWay = self.setDirection(way)
        currentPower = 0
        for product in range (1, self.power):
            tmpX = x + (xWay * product)
            tmpY = y + (yWay * product)
            if self.checkTheCell(tmpX, tmpY) == False:
                return currentPower
            currentPower += 1
        return currentPower


    def checkAround(self, x, y):
        if self.map[y][x] == "X" or self.map[y][x] == "O":
            return False
        for way in range (1, 9):
            currentPower = 1
            tmpWay = way
            currentPower += self.lastPowerCounter(x, y, way)
            tmpWay = self.reverseDirection(tmpWay)
            currentPower += self.lastPowerCounter(x, y, way)
            if currentPower >= self.power:
                return True
        return False

    def findGlobalOpportunity(self):
        for y in range (len(self.map)):
            for x in range (len(self.map[0])):
                if self.checkAround(x, y) == True:
                    self.selected_move = (y, x)
                    self.lastAttack.update({"x": x, "y": y})
                    self.map[y][x] = "O"
                    return True
        return False

    def lastMovesOfTheGame(self):
        for y in range (len(self.map)):
            for x in range (len(self.map[0])):
                if self.checkTheCell(x, y) == True:
                    self.selected_move = (y, x)
                    self.lastAttack.update({"x": x, "y": y})
                    self.map[y][x] = "O"
                    return True
        return False

    def lastChance(self, pos):
        if self.map[pos["y"]][pos["x"]] == "X":
            return False
        if self.findGlobalOpportunity() == True:
            return True
        if self.lastMovesOfTheGame() == True:
            return True
        return False
    
    # attempt
    def attack(self, pos, ways, factions):
        nth = random.randint(1, self.power)
        product = 0
        while nth > 0:
            tmpX = pos["x"] + (ways["x"] * product)
            tmpY = pos["y"] + (ways["y"] * product)
            if self.map[tmpY][tmpX] != factions["us"] and self.map[tmpY][tmpX] != factions["enemy"]:
                nth -= 1
            product += 1
            if product >= self.power:
                product = 0
        self.selected_move = (tmpY, tmpX)
        self.lastAttack.update({"x": tmpX, "y": tmpY})
        self.map[tmpY][tmpX] = "O"

    def verifInvalidPowers(self, pos, factions):
        if self.verifGoodPos(pos) == False:
            return True
        if self.map[pos["y"]][pos["x"]] == factions["enemy"]:
            return True
        return False

    def verifValidPowers(self, pos, factions):
        if self.verifGoodPos(pos) == False:
            return False
        if self.map[pos["y"]][pos["x"]] == factions["us"]:
            return True
        return False

    def verifPowers(self, factions, directions, tmpBestWay, pos):
        tmpInvalidNormal = self.verifInvalidPowers({"x":directions["xNormal"], "y":directions["yNormal"]}, factions)
        tmpValidNormal = self.verifValidPowers({"x":directions["xNormal"], "y":directions["yNormal"]}, factions)
        tmpInvalidInverse = self.verifInvalidPowers({"x":directions["xInverse"], "y":directions["yInverse"]}, factions)
        tmpValidInverse = self.verifValidPowers({"x":directions["xInverse"], "y":directions["yInverse"]}, factions)
        if tmpInvalidNormal == True and tmpInvalidInverse == True and directions["currentNormal"] + directions["currentInverse"] - 1 < self.power:
            return False
        if tmpInvalidNormal == True and tmpInvalidInverse == True and directions["currentNormal"] + directions["currentInverse"] - 1 >= self.power:
            directions["currentInverse"] -= 1
            directions["currentNormal"] -= 1
            directions["xNormal"] = pos["x"] + (directions["currentNormal"] * directions["xNormalWay"])
            directions["yNormal"] = pos["y"] + (directions["currentNormal"] * directions["yNormalWay"])
            tmpBestWay.update({"x": directions["xNormal"], "y": directions["yNormal"], "ways": {"x":directions["xNormalWay"], "y":directions["yNormalWay"]}})
        if tmpValidInverse == True:
            directions["currentNormal"] = directions["NormalSaved"]
            directions["currentPower"] += (directions["currentInverse"] - directions["currentPower"])
            directions["InverseSaved"] = directions["currentInverse"]
            tmpBestWay["power"] += 1
            tmpBestWay.update({"x": directions["xInverse"], "y": directions["yInverse"], "ways": {"x":directions["xInverseWay"], "y":directions["yInverseWay"]}})
            return True
        if tmpValidNormal == True:
            directions["currentInverse"] = directions["InverseSaved"]
            directions["currentPower"] += (directions["currentNormal"] - directions["NormalSaved"])
            directions["NormalSaved"] = directions["currentNormal"]
            tmpBestWay["power"] += 1
            tmpBestWay.update({"x": directions["xNormal"], "y": directions["yNormal"], "ways": {"x":directions["xNormalWay"], "y":directions["yNormalWay"]}})
            return True
        if (tmpInvalidNormal == True and tmpInvalidInverse == False):
            directions["currentNormal"] = directions["NormalSaved"]
            directions["currentPower"] += (directions["currentInverse"] - directions["currentPower"])
            directions["InverseSaved"] = directions["currentInverse"]
            tmpBestWay.update({"x": directions["xInverse"], "y": directions["yInverse"], "ways": {"x":directions["xInverseWay"], "y":directions["yInverseWay"]}})
            return True
        if (tmpInvalidNormal == False and tmpInvalidInverse == True):
            directions["currentInverse"] = directions["InverseSaved"]
            directions["currentPower"] += (directions["currentNormal"] - directions["NormalSaved"])
            directions["NormalSaved"] = directions["currentNormal"]
            tmpBestWay.update({"x": directions["xNormal"], "y": directions["yNormal"], "ways": {"x":directions["xNormalWay"], "y":directions["yNormalWay"]}})
            return True
        directions["currentPower"] += 1
        return True

    def compareBothPos(self, pos, factions, directions):
        tmpBestWay = {"x": pos["x"], "y": pos["y"], "power": 0, "ways": {"x": directions["xNormalWay"], "y": directions["yNormalWay"]}}
        for _ in range (1, self.power):
            directions["currentNormal"] += 1
            directions["currentInverse"] += 1
            directions["xNormal"] = pos["x"] + (directions["currentNormal"] * directions["xNormalWay"])
            directions["yNormal"] = pos["y"] + (directions["currentNormal"] * directions["yNormalWay"])
            directions["xInverse"] = pos["x"] + (directions["currentInverse"] * directions["xInverseWay"])
            directions["yInverse"] = pos["y"] + (directions["currentInverse"] * directions["yInverseWay"])
            if self.verifPowers(factions, directions, tmpBestWay, pos) == False:
                return
        if tmpBestWay["power"] >= self.bestWay["power"]:
            self.bestWay = tmpBestWay.copy()
            self.bestWay["ways"]["x"] *= -1
            self.bestWay["ways"]["y"] *= -1

    def stonePowerSearch(self, pos, factions, way):
        x, y = self.setDirection(way)
        directions = {"xNormalWay" : x, "yNormalWay" : y}
        way = self.reverseDirection(way)
        x, y = self.setDirection(way)
        directions.update({"xInverseWay" : x, "yInverseWay" : y})
        directions.update({'NormalSaved' : 0, 'InverseSaved' : 0})
        directions.update({'currentNormal' : 0, 'currentInverse' : 0})
        directions.update({"xNormal": 0, "yNormal" : 0, "xInverse" : 0, "yInverse" : 0})
        directions.update({"currentPower":1})
        self.compareBothPos(pos, factions, directions)

    def attempt(self, pos):
        self.bestWay = {"x": 0, "y": 0, "power": 0, "ways": {}}
        factions = self.setFactions(self.map[pos["y"]][pos["x"]])
        if len(factions) == 0:
            return False
        if factions["us"] != "O" or factions["enemy"] != "X":
            return False
        for way in range (1, 9):
            self.stonePowerSearch(pos, factions, way)
        if len(self.bestWay["ways"]) != 0:
            self.attack({"x":self.bestWay["x"], "y":self.bestWay["y"]}, self.bestWay["ways"], factions)
            return True
        return False
    
    # mainAlgorithm
    def game(self, pos):
        if self.lastMoves(pos) == True:
            return True
        if self.attempt(pos) == True:
            return True
        if self.lastChance(pos) == True:
            return True
        return False

    def algorithm(self, x = None, y = None):
        if x is None:
            x = self.lastAttack["x"]
        if y is None:
            y = self.lastAttack["y"]
        return self.game({"x": x, "y": y})

    def lastEnemyStone(self, x, y):
        self.editMap({"x": x, "y":y}, "X")

    def verifLastMoves(self):
        x = self.lastAttack["x"]
        y = self.lastAttack["y"]
        return self.lastMoves({"x": x, "y":y})

    def setupMap(self):
        x, y = 0, 0
        for line in self.map:
            x = 0
            for cell in line:
                if cell == "O" and self.lastMoves({"x":x, "y":y}) == True:
                    return True
                x += 1
            y += 1
        y = 0
        for line in self.map:
            x = 0
            for cell in line:
                if cell == "X" and self.lastMoves({"x":x, "y":y}, True) == True:
                    return True
                x += 1
            y += 1
        return False

    def next_turn(self, x, y, firstRound = False):
        if firstRound == False:
            self.lastEnemyStone(x, y)
        if self.setupMap() == True:
            return
        if self.algorithm(x, y) == True:
            return
        self.algorithm()