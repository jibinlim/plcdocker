import {
  Controller,
  Post,
  Req,
  Body,
  Get,
  Patch,
  Delete,
} from '@nestjs/common';
import { UserDTO, ChangPwd } from './dto/user.dto';
import { AuthService } from './auth.service';
import { Request } from '@nestjs/common';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('/sign-up')
  async singup(
    @Req() req: Request,
    @Body() UserDTO: UserDTO,
  ): Promise<UserDTO> {
    return await this.authService.registerUser(UserDTO);
  }

  @Post('/login')
  async login(
    @Body() UserDTO: UserDTO,
  ): Promise<{ accessToken: string } | undefined> {
    return await this.authService.validateUser(UserDTO);
  }

  @Patch('/update')
  async update(
    @Req() req: Request,
    @Body() ChangPwd: ChangPwd,
  ): Promise<string> {
    return await this.authService.updateUser(ChangPwd);
  }

  // @Delete('/deleteUser')
  // async del(
  //   @Req() req: Request,
  //   @Body() UserDTO: UserDTO,
  // ): Promise<string | undefined> {
  //   return await this.authService.deleteUser(UserDTO);
  // }
}
