import sqlite3
from subprocess import Popen, PIPE
from _curses import start_color


class WinTixTracker():
    
    def __init__(self):
        self.game1 = 'masscash'
        self.game2 = 'megamillions'
        self.game3 = 'powerball'
        self.num_size = 70
    def enter_bulk_winning_numbers(self):
        """This method will accept either a single winning ticket as input or 
           a block of winning number and store them in a database """
           
        win_tix = int(input("Please enter one or more winning ticket numbers."))
        while(win_tix > 0):
            n = int(input())
            arr = list(map(int,input().strip().split(' ')))
            arr.remove(max(arr))
            print(max(arr))
            win_tix -= 1
            
    def enter_selected_no_win_numbers(self):
         """This method will accept a number as input or 
           a block of winning number and store them in a database """
           
         no_win_no = int(input("Please enter a number that was selected by the algorithm but did not win "))
         # Update the tally of no_wins for that number in the database by + 1 
    def update_win_tally_for_no(self, win_num):
          # Increase the tally for the winning number by 1
          print("""Hello""")
    def calc_win_probs(self, game = 'masscash'):
        if (game == 'masscash'):
            self.num_size = 35
            self.magic_ball_sz = 0
            p1 =Popen(["cat mass_cash.txt | awk '{print $3}' | wc -l"], shell=True, stdout= PIPE)
            p2 =Popen(["cat mass_cash.txt | awk '{print $3}'"], shell=True, stdout= PIPE)
            
        elif (game == 'powerball'): # powerball 26
            self.numsize = 69
            self.magic_ball_sz = 26
            p1 =Popen(["cat powerball.txt | awk '{print $3}' | wc -l"], shell=True, stdout= PIPE)
            p2 =Popen(["cat powerball.txt | awk '{print $3}'"], shell=True, stdout= PIPE)
            
        elif (game =='megamillions'): # 
            self.num_size = 70
            self.magic_ball_sz = 25
        else:
            print("Unsupported game")
            return 1
        
        
#         p1 =Popen(["ls -altr"], shell=True, stdout= PIPE)
#         print(p1.communicate())
        #p1 =Popen(["cat mass_cash.txt | awk '{print $3}' | wc -l"], shell=True, stdout= PIPE)
#         game_file = game+".txt"
#         p1 =Popen(["cat powerball.txt | awk '{print $3}' | wc -l"], shell=True, stdout= PIPE)
        self.result_pool_sz = (p1.communicate())[0]
        print("self.result_pool_sz %s",self.result_pool_sz)
        self.result_pool_sz = self.result_pool_sz.strip().decode('ascii')
        print("There are a total of %s lottery results.",self.result_pool_sz)
        lotto_num_probs = { i:0 for i in range(1,self.num_size)}
        key_lotto_num_probs = lotto_num_probs.keys()
        print("key_lotto_num_probs ",key_lotto_num_probs)
        for ball in range(1,6):
            
            #p1 =Popen(["cat mass_cash.txt | awk '{print $3}'"], shell=True, stdout= PIPE)
            p1 =Popen(["cat mass_cash.txt | awk '{print $3}' | wc -l"], shell=True, stdout= PIPE)
            p2 =Popen(["cat mass_cash.txt | awk '{print $3}'"], shell=True, stdout= PIPE)
            cmd2 = (f"cut -d'-' -f {ball}")
            p3 = Popen([cmd2], stdin=p2.stdout, shell= True, stdout= PIPE)
            #p2.stdout.close()
            self.ball_results_lst = (p3.communicate())[0]
            self.ball_results_lst = self.ball_results_lst.strip().decode('ascii')
            # Convert to list
            self.ball_results_lst = list(self.ball_results_lst.split("\n"))
            print("self.ball_results_lst ",self.ball_results_lst)
            for ball_num in range(1,self.num_size+1):
                ball_count=self.ball_results_lst.count(ball_num)
                # Calculate probability and store in dict
                ball_num = int(ball_num)
                self.result_pool_sz = float(self.result_pool_sz)
                prob_num = ball_count/(self.result_pool_sz)
                lotto_num_probs[ball_num]= prob_num
                
            # Find best no by ranges
            num_ranges = (self.num_size//10)+1
            count  = 0
            k_start  = 1
            k_stop = 10
            print("="*70)
            while count < num_ranges:
                
                curr_lotto_num_probs= {k:lotto_num_probs[k] for k in range (k_start, k_stop)}
                print("curr_lotto_num_probs{curr_lotto_num_probs}")
                range_best_no=max(curr_lotto_num_probs, key=curr_lotto_num_probs.get)
                print("For numbers ",k_start," to ",k_stop," the best number is ",range_best_no)
                del curr_lotto_num_probs[range_best_no]
                range_best_no=max(curr_lotto_num_probs, key=curr_lotto_num_probs.get)
                print("For numbers ",k_start," to ",k_stop," the best number is ",range_best_no)
                del curr_lotto_num_probs[range_best_no]
                range_best_no=max(curr_lotto_num_probs, key=curr_lotto_num_probs.get)
                print("For numbers ",k_start," to ",k_stop," the best number is ",range_best_no)
                count +=1
                k_start+=10
                k_stop+=10
                if k_stop > self.num_size:
                    k_stop = self.num_size
                
            
            best_no=max(lotto_num_probs, key=lotto_num_probs.get)
            print("Ball Number :", ball, "Best Number ", best_no)
            del lotto_num_probs[best_no]
            best_no=max(lotto_num_probs, key=lotto_num_probs.get)
            print("Ball Number :", ball, "2nd Best Number", best_no)
            del lotto_num_probs[best_no]
            best_no=max(lotto_num_probs, key=lotto_num_probs.get)
            print("Ball Number :", ball, "3rd Best Number", best_no)
            
        if self.magic_ball_sz != 0:
             
            p1 =Popen(["cat powerball.txt | awk '{print $4}'"], shell=True, stdout= PIPE)
            powerball_results_lst = (p1.communicate())[0]   
            powerball_results_lst = powerball_results_lst.strip().decode('ascii')
            powerball_results_lst = list(powerball_results_lst.split("\n"))
            magic_num_probs = { i:0 for i in range(1,self.magic_ball_sz)}
            for magic_ball_num in range(1,self.magic_ball_sz+1): 
                magic_ball_count=powerball_results_lst.count(magic_ball_num)
                prob_magic_num = magic_ball_count/(self.result_pool_sz)    
                magic_num_probs[magic_ball_num]= prob_magic_num
                
                
            
            best_magic_no=max(magic_num_probs, key=magic_num_probs.get)
            print("-+-"*70)
            print("Magic Ball Number : 1 Best Number", best_magic_no)
            del magic_num_probs[best_magic_no]
            print("-+-"*70)
            best_magic_no=max(magic_num_probs, key=magic_num_probs.get)
            print("Magic Ball Number : 2 Best Number", best_magic_no)
            del magic_num_probs[best_magic_no]
            print("-+-"*70)
            best_magic_no=max(magic_num_probs, key=magic_num_probs.get)
            print("Magic Ball Number : 3 Best Number", best_magic_no)
            del magic_num_probs[best_magic_no]
            print("-+-"*70)
            best_magic_no=max(magic_num_probs, key=magic_num_probs.get)
            print("Magic Ball Number : 4 Best Number", best_magic_no)
            del magic_num_probs[best_magic_no]
            print("-+-"*70)
            best_magic_no=max(magic_num_probs, key=magic_num_probs.get)
            print("Magic Ball Number : 5 Best Number", best_magic_no)
            del magic_num_probs[best_magic_no]
            #print(f" POWERBALL :{}")
#             
        
#         self.pool_of_past_winning_tix 
#         _lst_by_col_x = []
#         _lst_by_col_x = f"cat mass_cash.txt | awk '{print $3}' | cut -d'-' -f{i}"
#         for i in range(num_size):
#             #Start from column 1 calculate the probability of each number
#     def calc_win_probs_for_ranges(self, game = 'masscash'):
#            