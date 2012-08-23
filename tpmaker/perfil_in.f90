program inicio
!use IFPORT
implicit none
integer i,j,k,nx,ny,nz,idum,nv
real lx,ly,lz,theta,R,D,u1,u2,ra,ale,eps,centro,ruido
!real,allocatable,dimension(:)::x,y,z
real,allocatable,dimension(:,:,:)::u,v,w,p,t,x,y,z

nx = 150
ny = 109
nz = 109
lx=8.0
ly=4.0
lz=4.0


allocate(x(nx,ny,nz))
allocate(y(nx,ny,nz))
allocate(z(nx,ny,nz))
allocate(u(nx,ny,nz))
allocate(v(nx,ny,nz))
allocate(w(nx,ny,nz))
allocate(p(nx,ny,nz))
allocate(t(nx,ny,nz))
open(66,file='jet.grid',form='unformatted')
read(66)nv
read(66)nx,ny,nz
    read(66)x
    read(66)y
    read(66)z
close(66)
u1=1.
u2=-1.
D=2.
R=D/2.
centro=lz/2.
theta=1.*0.25
ruido=0.5
eps=0.1
idum=0.1
write(*,*)'u1',u1
write(*,*)'u2',u2
write(*,*)'D',D
write(*,*)'R',R
write(*,*)'theta',theta
write(*,*)'centro',centro
write(*,*)'ruido',ruido
do k=1,nz
   do j=1,ny
      do i=1,nx
         ale=ran(idum)
         ra=z(i,j,k)-centro
         u(i,j,k)=(u1+u2)/2.+(u1-u2)/2.*tanh(theta*(ra/R-R/ra))
         v(i,j,k)=0.
         w(i,j,k)=0.
         if(z(i,j,k).ge.centro)u(i,j,k)=-u(i,j,k)
         if((z(i,j,k).ge.centro-R*(1.+ruido)).and.&
            (z(i,j,k).le.centro-R*(1.-ruido)))then
            u(i,j,k)=u(i,j,k)+eps*(ale-0.5)
            v(i,j,k)=v(i,j,k)+eps*(ale-0.5)
            w(i,j,k)=w(i,j,k)+eps*(ale-0.5)
         end if
         if((z(i,j,k).le.centro+R*(1.+ruido)).and.&
            (z(i,j,k).ge.centro+R*(1.-ruido)))then
            u(i,j,k)=u(i,j,k)+eps*(ale-0.5)
            v(i,j,k)=v(i,j,k)+eps*(ale-0.5)
            w(i,j,k)=w(i,j,k)+eps*(ale-0.5)
         end if
         p(i,j,k)=1.0
         t(i,j,k)=1.0
      end do
   end do
end do
close(67)
do k=1,nz
!  write(*,*)k,u(1,1,k)
end do
open(68,file='field_000.bin',form='unformatted')
write(68)nv
write(68)nx,ny,nz
write(68)u
write(68)v
write(68)w
write(68)t
write(68)p
close(68)
write(*,*)'Condiciones Iniciales Creadas ->> field_0.000'
deallocate(x)
deallocate(y)
deallocate(z)
deallocate(u)
deallocate(v)
deallocate(w)
deallocate(p)
deallocate(t)
end
!____________________________________________________________________

!____________________________________________________________________

function ran(idum)
implicit none
integer,parameter::k4b=selected_int_kind(9)
integer(k4b),intent(inout)::idum
real::ran
integer(k4b),parameter::ia=16807,im=2147483647,Iq=127773,IR=2836
real,save::am
integer(k4b),save::ix=-1,iy=-1,k
if(idum.le.0.or.iy.le.0)then
am=nearest(1.0,-1.0)/IM
iy=ior(ieor(888889999,abs(idum)),1)
ix=ieor(77775555,abs(idum))
idum=abs(idum)+1
end if
ix=ieor(ix,ishft(ix,13))
ix=ieor(ix,ishft(ix,-17))
ix=ieor(ix,ishft(ix,5))
k=iy/iq
iy=ia*(iy-k*iq)-ir*k
if(iy.le.0.)iy=iy+im
ran=am*ior(iand(im,ieor(ix,iy)),1)
return
end function

