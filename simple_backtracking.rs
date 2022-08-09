pub fn to_string(board:&mut Vec<Vec<u8>>) ->String{
    let mut board_str=String::new();
    for i in board{
        i.iter()
        .for_each(|x| if *x==0 {
                        board_str.push('.');
                    }else{
                        board_str.push('Q');
                    });
        board_str.push('\n');
    }
    return board_str;
}

pub fn is_safe( row:usize, col:usize, queenpos:&mut Vec<(usize,usize)>)->bool{
    for x in queenpos{
        if ((x.0 as i32)-(col as i32)).abs()==((x.1 as i32)-(row as i32)).abs(){
            return false;
        }
        if x.1==row{
            return false;
        }
    }
    return true;
}

pub fn solve_nq_util(board:&mut Vec<Vec<u8>>,mut col:usize,n:usize,num:usize, queenpos:&mut Vec<(usize,usize)>)->bool{
    if col>=n{
        col=col-n;
    }
    if num>=n{
        return true;
    }
     for i in 0..n{
        if is_safe(i, col,queenpos){
            board[i][col] = 1;
            queenpos.push((col,i));
            if solve_nq_util(board, col + 1, n,num+1,queenpos)==false{
                board[i][col] = 0;
                queenpos.pop();
            }else{
                return true;
            }
        }
    }
    return false;
}           



        
        
        
pub fn solve_n_queens(n: usize, mandatory_coords: (usize, usize)) -> Option<String> {
    let mut board = vec![vec![0 as u8; n]; n];
    let mut queenpos=vec![mandatory_coords];
    board[mandatory_coords.1][mandatory_coords.0]=1;
    if solve_nq_util(&mut board, mandatory_coords.0+1,n,1,&mut queenpos)==false{
        return None;
    }
     println!("{}",to_string(&mut board));
    return Some(to_string(&mut board));
}
