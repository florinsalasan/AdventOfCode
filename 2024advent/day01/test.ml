let inc x = x + 1;;

let print_and_return x = 
    print_endline (string_of_int x);
    x
;;

print_and_return(inc 10);;
