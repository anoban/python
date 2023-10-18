def odd(number: int) -> bool:
    return number % 2 != 0


if __name__ == "__main__":
    odd(65.6547645)
    odd("odd")
    
    for i in range(100):
        print(odd(i))
        
        